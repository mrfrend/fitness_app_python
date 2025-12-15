from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QDate, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QDateEdit,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ClientInfoUi(QMainWindow):
    client_saved = pyqtSignal(dict)
    back_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Данные клиента")
        self.setMinimumSize(520, 520)

        self._client_id: Optional[int] = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(16)
        grid_layout.setVerticalSpacing(12)
        main_layout.addLayout(grid_layout)

        self.client_id_input = QLineEdit()
        self.client_id_input.setReadOnly(True)

        self.last_name_input = QLineEdit()
        self.first_name_input = QLineEdit()
        self.middle_name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.birth_date_input = QDateEdit(calendarPopup=True)
        self.birth_date_input.setDisplayFormat("dd.MM.yyyy")
        self.birth_date_input.setDate(QDate.currentDate().addYears(-18))
        self.health_limits_input = QLineEdit()

        labels_and_editors = (
            (QLabel("ID клиента:"), self.client_id_input),
            (QLabel("Фамилия:"), self.last_name_input),
            (QLabel("Имя:"), self.first_name_input),
            (QLabel("Отчество:"), self.middle_name_input),
            (QLabel("Телефон:"), self.phone_input),
            (QLabel("Email:"), self.email_input),
            (QLabel("Дата рождения:"), self.birth_date_input),
            (QLabel("Мед. ограничения:"), self.health_limits_input),
        )

        for row, (label, editor) in enumerate(labels_and_editors):
            grid_layout.addWidget(label, row, 0, alignment=Qt.AlignmentFlag.AlignRight)
            grid_layout.addWidget(editor, row, 1)

        buttons_layout = QHBoxLayout()
        self.btnSave = QPushButton("Сохранить")
        self.btnBack = QPushButton("Назад")
        buttons_layout.addWidget(self.btnSave)
        buttons_layout.addWidget(self.btnBack)
        main_layout.addLayout(buttons_layout)

        self.btnSave.clicked.connect(self._on_save)
        self.btnBack.clicked.connect(self._on_back)

        self.styleApply()

    def set_client_id(self, client_id: int) -> None:
        self._client_id = int(client_id)
        self.client_id_input.setText(str(client_id))

    def styleApply(self):
        self.setStyleSheet(
            """
            QWidget {
                font-family: Segoe UI;
                font-size: 14px;
            }

            QDateEdit, QLineEdit {
                padding: 6px;
                border: 1px solid #aaa;
                border-radius: 6px;
            }

            QPushButton {
                background-color: #3855c7;
                color: white;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 15px;
            }

            QPushButton:hover {
                background-color: #2563eb;
            }

            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            """
        )

    def _on_save(self) -> None:
        if self._client_id is None:
            QMessageBox.warning(self, "Ошибка", "Не задан ID клиента")
            return

        required = [self.last_name_input, self.first_name_input, self.phone_input]
        if any(not field.text().strip() for field in required):
            QMessageBox.warning(self, "Ошибка", "Заполните фамилию, имя и телефон")
            return

        data = {
            "userID": int(self._client_id),
            "first_name": self.first_name_input.text().strip(),
            "last_name": self.last_name_input.text().strip(),
            "middle_name": self.middle_name_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "email": self.email_input.text().strip(),
            "birth_date": self.birth_date_input.date().toPyDate(),
            "health_limits": self.health_limits_input.text().strip(),
        }

        self.client_saved.emit(data)

    def _on_back(self) -> None:
        self.back_requested.emit()
        self.close()

    def closeEvent(self, event):
        self.back_requested.emit()
        event.accept()
