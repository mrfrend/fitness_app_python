from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QTableWidget, QHeaderView)
from PyQt6.QtCore import Qt
import sys


class ManageClient(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Управление клиентами")
        self.setMinimumSize(900, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        buttons_layout = QHBoxLayout()
        self.btnAdd = QPushButton("Добавить клиента")
        self.btnInfo = QPushButton("Данные клиента")
        self.btnEdit = QPushButton("Изменить абонемент")
        self.btnCard = QPushButton("Распечатать клубную карту")
        self.btnFreeze = QPushButton("Заморозить абонемент")
        self.btnBack = QPushButton("Назад")

        for button in (self.btnAdd, self.btnInfo, self.btnEdit, self.btnCard, self.btnFreeze, self.btnBack):
            button.setMinimumWidth(170)
            buttons_layout.addWidget(button)

        main_layout.addLayout(buttons_layout)

        self.tableWidget = QTableWidget(0, 5)
        self.tableWidget.setHorizontalHeaderLabels([
            'ID', 'Фамилия', 'Имя', 'Телефон', 'Абонемент'
        ])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableWidget.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setAlternatingRowColors(True)
        main_layout.addWidget(self.tableWidget)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ManageClient()
    window.show()
    sys.exit(app.exec())