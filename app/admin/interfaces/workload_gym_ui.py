from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout,
                             QLineEdit, QPushButton, QDateEdit, QGridLayout, QTableWidget, QTableWidgetItem, QTextEdit)
from PyQt6.QtCore import Qt, QDate
import sys


class WorkloadUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Загруженность залов")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.main_label = QLabel("Загруженность залов")
        main_layout.addWidget(self.main_label)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Зона', 'Дата начала', 'Дата окончания', 'Описание'
        ])
        main_layout.addWidget(self.table)

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(16)
        form_layout.setVerticalSpacing(12)
        main_layout.addLayout(form_layout)

        self.zone_label = QLabel("Зона")
        self.zone_select = QComboBox()
        form_layout.addWidget(self.zone_label, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
        form_layout.addWidget(self.zone_select, 0, 1)

        self.start_label = QLabel("Дата начала")
        self.start_date = QDateEdit(calendarPopup=True)
        self.start_date.setDate(QDate.currentDate())
        form_layout.addWidget(self.start_label, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        form_layout.addWidget(self.start_date, 1, 1)

        self.end_label = QLabel("Дата окончания")
        self.end_date = QDateEdit(calendarPopup=True)
        self.end_date.setDate(QDate.currentDate())
        form_layout.addWidget(self.end_label, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        form_layout.addWidget(self.end_date, 2, 1)

        self.info_label = QLabel("Описание")
        self.info_input = QTextEdit()
        form_layout.addWidget(self.info_label, 3, 0, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        form_layout.addWidget(self.info_input, 3, 1)

        btn_layout = QHBoxLayout()
        self.btnAdd = QPushButton("Добавить запись")
        self.btnAdd.setObjectName('btnAdd')
        btn_layout.addWidget(self.btnAdd)

        self.btnUpdate = QPushButton("Обновить запись")
        btn_layout.addWidget(self.btnUpdate)

        self.btnDelete = QPushButton("Удалить запись")
        btn_layout.addWidget(self.btnDelete)

        btn_layout.addStretch(1)
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
                color: #fff;
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
    window = WorkloadUi()
    window.show()
    sys.exit(app.exec())