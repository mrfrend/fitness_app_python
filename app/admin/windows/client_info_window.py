from __future__ import annotations

from datetime import date
from typing import Any, Dict, Optional

from PyQt6.QtCore import QDate, pyqtSignal
from PyQt6.QtWidgets import QMessageBox

from app.admin.db_objects.database_for_me import db
from app.admin.interfaces.client_info_ui import ClientInfoUi


class ClientInfoWindow(ClientInfoUi):
    client_updated = pyqtSignal()

    def __init__(self, client_id: int, parent=None):
        super().__init__(parent)
        self._client_id = int(client_id)

        self.set_client_id(self._client_id)
        self.client_saved.connect(self._save_client)

        self._load_client()

    def _load_client(self) -> None:
        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT userID,
                           first_name,
                           last_name,
                           middle_name,
                           phone,
                           email,
                           birthDate,
                           health_limits
                    FROM Users
                    WHERE userID = %s AND userType = 'Client'
                    """,
                    (self._client_id,),
                )
                client = cursor.fetchone()

            if not client:
                QMessageBox.warning(self, "Ошибка", "Клиент не найден")
                self.close()
                return

            self.last_name_input.setText(str(client.get("last_name") or ""))
            self.first_name_input.setText(str(client.get("first_name") or ""))
            self.middle_name_input.setText(str(client.get("middle_name") or ""))
            self.phone_input.setText(str(client.get("phone") or ""))
            self.email_input.setText(str(client.get("email") or ""))
            self.health_limits_input.setText(str(client.get("health_limits") or ""))

            birth_date = client.get("birthDate")
            if isinstance(birth_date, date):
                self.birth_date_input.setDate(QDate(birth_date.year, birth_date.month, birth_date.day))

        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные клиента: {exc}")

    def _save_client(self, data: Dict[str, Any]) -> None:
        try:
            with db.conn.cursor() as cursor:
                cursor.callproc(
                    "UpdateClient",
                    (
                        int(data["userID"]),
                        data.get("first_name", ""),
                        data.get("last_name", ""),
                        data.get("middle_name", ""),
                        data.get("phone", ""),
                        data.get("email", ""),
                        data.get("birth_date"),
                        data.get("health_limits", ""),
                    ),
                )

            db.conn.commit()
            QMessageBox.information(self, "Успех", "Данные клиента сохранены")
            self.client_updated.emit()
            self._on_back()
        except Exception as exc:
            db.conn.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить данные клиента: {exc}")
