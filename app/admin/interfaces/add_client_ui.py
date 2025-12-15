from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QDateEdit, QGridLayout,
                             QMessageBox)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
import sys


class AddClientWindow(QMainWindow):
    client_added = pyqtSignal(dict)
    back_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить клиента")
        self.setMinimumSize(420, 520)
        self.save_succeeded = False

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(16)
        grid_layout.setVerticalSpacing(12)
        main_layout.addLayout(grid_layout)

        self.inputs = {
            "last_name": (QLabel("Фамилия"), QLineEdit()),
            "first_name": (QLabel("Имя"), QLineEdit()),
            "middle_name": (QLabel("Отчество"), QLineEdit()),
            "birth": (QLabel("Дата рождения"), QDateEdit(calendarPopup=True)),
            "phone": (QLabel("Телефон"), QLineEdit()),
            "email": (QLabel("Email"), QLineEdit()),
            "goal": (QLabel("Цель занятий"), QLineEdit()),
            "limits": (QLabel("Мед. ограничения"), QLineEdit())
        }

        self.inputs["birth"][1].setDisplayFormat("dd.MM.yyyy")
        self.inputs["birth"][1].setDate(QDate.currentDate().addYears(-18))

        for row, (label, editor) in enumerate(self.inputs.values()):
            grid_layout.addWidget(label, row, 0, alignment=Qt.AlignmentFlag.AlignRight)
            grid_layout.addWidget(editor, row, 1)

        button_layout = QGridLayout()
        self.btnCreate = QPushButton("Создать")
        self.btnBack = QPushButton("Назад")
        button_layout.addWidget(self.btnCreate, 0, 0)
        button_layout.addWidget(self.btnBack, 0, 1)
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)

        self.btnCreate.clicked.connect(self._on_create)
        self.btnBack.clicked.connect(self.close)

        self.styleApply()

    def styleApply(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                font-size: 14px;
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
        """)

    def _on_create(self):
        required = [self.inputs["last_name"][1], self.inputs["first_name"][1], self.inputs["phone"][1]]
        if any(not field.text().strip() for field in required):
            QMessageBox.warning(self, "Ошибка", "Заполните фамилию, имя и телефон")
            return

        self.save_succeeded = False
        data = {
            "last_name": self.inputs["last_name"][1].text().strip(),
            "first_name": self.inputs["first_name"][1].text().strip(),
            "middle_name": self.inputs["middle_name"][1].text().strip(),
            "birth_date": self.inputs["birth"][1].date().toPyDate(),
            "phone": self.inputs["phone"][1].text().strip(),
            "email": self.inputs["email"][1].text().strip(),
            "goal": self.inputs["goal"][1].text().strip(),
            "health_limits": self.inputs["limits"][1].text().strip()
        }

        self.client_added.emit(data)
        if self.save_succeeded:
            self.close()

    def closeEvent(self, event):
        self.back_requested.emit()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddClientWindow()
    window.show()
    sys.exit(app.exec())