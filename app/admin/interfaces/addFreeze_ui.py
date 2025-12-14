from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, \
    QPushButton, QDateEdit, QGridLayout
from PyQt6.QtCore import Qt
import sys


class AddFreeze(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить заморозку")


        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(15)
        main_layout.addLayout(grid_layout)

        self.client = QLabel("Id клиента")
        self.f_enter = QLabel("№")

        self.dateOn = QLabel("Дата начала")
        self.dateOnEnter = QDateEdit()

        self.dateEnd = QLabel("Дата конца")
        self.dateEndEnter = QDateEdit()

        self.reson = QLabel("Причина")
        self.resonEnter = QLabel("причина")

        labels = [
            self.client, self.dateOn, self.dateEnd, self.reson
        ]

        values = [
            self.f_enter, self.dateOnEnter, self.dateEndEnter, self.resonEnter
        ]

        for row, (lbl, val) in enumerate(zip(labels, values)):
            grid_layout.addWidget(lbl, row, 0, alignment=Qt.AlignmentFlag.AlignRight)
            grid_layout.addWidget(val, row, 1)

        btn_layout = QHBoxLayout()
        self.btnSave = QPushButton("Сохранить")
        btn_layout.addWidget(self.btnSave)
        self.btnBack = QPushButton("Назад")
        btn_layout.addWidget(self.btnBack)
        main_layout.addLayout(btn_layout)

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
    window = AddFreeze()
    window.show()
    sys.exit(app.exec())