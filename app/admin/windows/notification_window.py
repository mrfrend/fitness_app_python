
from __future__ import annotations

from typing import List, Optional, Tuple

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from app.admin.db_objects.database_for_me import db
from app.admin.interfaces.notification_ui import NotificatioUi


class NotificationWindow(NotificatioUi):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        self._recipients: List[Tuple[Optional[int], str]] = []

        self._setup_connections()
        self._load_recipients()

    def _setup_connections(self) -> None:
        if hasattr(self, "btnBack"):
            self.btnBack.clicked.connect(self._go_back)
        if hasattr(self, "btnSend"):
            self.btnSend.clicked.connect(self._send_notification)
        if hasattr(self, "btnDelete"):
            self.btnDelete.clicked.connect(self._clear_form)

    def _load_recipients(self) -> None:
        self.send_to_combo.clear()
        self._recipients = []

        self._recipients.append((None, "Всем клиентам"))
        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT userID, last_name, first_name, phone
                    FROM Users
                    WHERE userType = 'Client'
                    ORDER BY last_name, first_name
                    """
                )
                rows = cursor.fetchall()

            for row in rows:
                user_id = int(row.get("userID"))
                last_name = str(row.get("last_name") or "")
                first_name = str(row.get("first_name") or "")
                phone = str(row.get("phone") or "")
                label = f"{last_name} {first_name} ({phone})".strip()
                self._recipients.append((user_id, label))

        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список клиентов: {exc}")

        for user_id, label in self._recipients:
            self.send_to_combo.addItem(label, user_id)

        self.send_to_combo.setCurrentIndex(0)

    def _send_notification(self) -> None:
        message = self.text_enter.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "Ошибка", "Текст уведомления не должен быть пустым")
            return

        selected_user_id = self.send_to_combo.currentData(Qt.ItemDataRole.UserRole)

        try:
            with db.conn.cursor() as cursor:
                if selected_user_id is None:
                    cursor.execute("SELECT userID FROM Users WHERE userType = 'Client' ORDER BY userID")
                    user_ids = [int(row.get("userID")) for row in cursor.fetchall()]
                    if not user_ids:
                        QMessageBox.warning(self, "Внимание", "Нет клиентов для рассылки")
                        return

                    cursor.executemany(
                        "INSERT INTO Notifications (userID, message_n) VALUES (%s, %s)",
                        [(user_id, message) for user_id in user_ids],
                    )
                else:
                    cursor.execute(
                        "INSERT INTO Notifications (userID, message_n) VALUES (%s, %s)",
                        (int(selected_user_id), message),
                    )

            db.conn.commit()
            QMessageBox.information(self, "Успех", "Уведомление отправлено")
            self._clear_form()
        except Exception as exc:
            db.conn.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось отправить уведомление: {exc}")

    def _clear_form(self) -> None:
        self.send_to_combo.setCurrentIndex(0)
        self.text_enter.clear()

    def _go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()

    def closeEvent(self, event):
        if self.parent_window:
            self.parent_window.show()
        event.accept()
