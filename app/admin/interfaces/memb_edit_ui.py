from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QHBoxLayout, QLineEdit, QDateEdit, QPushButton)
from PyQt6.QtCore import pyqtSignal, QDate
import sys


class MembEdit(QMainWindow):
    membership_updated = pyqtSignal()
    back_requested = pyqtSignal()

    def __init__(self, client_id=None, parent=None):
        super().__init__(parent)
        self.client_id = client_id
        self.setWindowTitle("Изменение абонемента")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        title = QLabel("Изменение абонемента")
        main_layout.addWidget(title)

        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Новый тип:"))
        self.type_input = QLineEdit()
        type_layout.addWidget(self.type_input)
        main_layout.addLayout(type_layout)

        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Начало:"))
        self.start_date = QDateEdit(calendarPopup=True)
        self.start_date.setDate(QDate.currentDate())
        start_layout.addWidget(self.start_date)
        main_layout.addLayout(start_layout)

        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("Конец:"))
        self.end_date = QDateEdit(calendarPopup=True)
        self.end_date.setDate(QDate.currentDate().addMonths(1))
        end_layout.addWidget(self.end_date)
        main_layout.addLayout(end_layout)

        btn_layout = QHBoxLayout()
        self.btnSave = QPushButton("Сохранить")
        self.btnBack = QPushButton("Назад")
        btn_layout.addWidget(self.btnSave)
        btn_layout.addWidget(self.btnBack)
        main_layout.addLayout(btn_layout)

        self.btnSave.clicked.connect(self._on_save)
        self.btnBack.clicked.connect(self._on_back)

        self.styleApply()

    def styleApply(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                font-size: 14px;
            }

            QDateEdit {
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
        """)

    def _on_save(self):
        # Логика обновления абонемента может быть добавлена здесь.
        self.membership_updated.emit()
        self._on_back()

    def _on_back(self):
        self.back_requested.emit()
        self.close()

    def closeEvent(self, event):
        self.back_requested.emit()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MembEdit()
    window.show()
    sys.exit(app.exec())