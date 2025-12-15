from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QComboBox, QDateEdit, QTextEdit)
from PyQt6.QtCore import QDate
import sys

class ScheduleUi(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(['ID', 'Дата', 'Описание', 'Тренер'])
        main_layout.addWidget(self.table)

        form_layout = QVBoxLayout()

        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Дата занятия:"))
        self.date_input = QDateEdit(calendarPopup=True)
        self.date_input.setDate(QDate.currentDate())
        date_layout.addWidget(self.date_input)
        form_layout.addLayout(date_layout)

        desc_layout = QVBoxLayout()
        desc_label = QLabel("Описание занятия:")
        self.description_input = QTextEdit()
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.description_input)
        form_layout.addLayout(desc_layout)

        trainer_layout = QHBoxLayout()
        trainer_layout.addWidget(QLabel("Тренер:"))
        self.trainer_select = QComboBox()
        trainer_layout.addWidget(self.trainer_select)
        form_layout.addLayout(trainer_layout)

        main_layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btnAdd = QPushButton("Добавить занятие")
        btn_layout.addWidget(self.btnAdd)
        self.btnDelete = QPushButton("Удалить занятие")
        btn_layout.addWidget(self.btnDelete)
        main_layout.addLayout(btn_layout)

        back_layout = QHBoxLayout()
        self.btnBack = QPushButton("Назад")
        back_layout.addStretch(1)
        back_layout.addWidget(self.btnBack)
        main_layout.addLayout(back_layout)

        self.styleApply()

    def styleApply(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                font-size: 14px;
            }

            QLabel {
                font-size: 18px;
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScheduleUi()
    window.show()
    sys.exit(app.exec())
