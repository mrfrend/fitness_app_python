from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QLineEdit, \
    QPushButton, QDateEdit, QGridLayout
from PyQt6.QtCore import Qt
import sys


class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пользователь")


        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)


        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(15)
        main_layout.addLayout(grid_layout)

        self.fio_text = QLabel("ФИО:")
        self.fio_enter = QLabel("Иванов Сергей Петрович")

        self.rost_text = QLabel("Рост:")
        self.rost_enter = QLabel("190")

        self.birth_text = QLabel("Дата рождения:")
        self.birth_enter = QDateEdit()

        self.goal_text = QLabel("Цель занятий:")
        self.goal_enter = QLabel("Мышцы хочу")

        self.email_text = QLabel("Email:")
        self.email_enter = QLabel("ivanovsergay190@mail.ru")

        self.phone_text = QLabel("Телефон:")
        self.phone_enter = QLabel("89261726312")

        self.med_text = QLabel("Мед. ограничения:")
        self.med_enter = QLabel("Нет")

        labels = [
            self.fio_text, self.rost_text, self.birth_text,
            self.goal_text, self.email_text, self.phone_text, self.med_text
        ]

        values = [
            self.fio_enter, self.rost_enter, self.birth_enter,
            self.goal_enter, self.email_enter, self.phone_enter, self.med_enter
        ]

        for row, (lbl, val) in enumerate(zip(labels, values)):
            grid_layout.addWidget(lbl, row, 0, alignment=Qt.AlignmentFlag.AlignRight)
            grid_layout.addWidget(val, row, 1)


        self.btnZapis = QPushButton("Запись на занятие")
        self.btnMyZan = QPushButton("Мои занятия")
        self.btnHistory = QPushButton("История посещений")

        main_layout.addWidget(self.btnZapis)
        main_layout.addWidget(self.btnMyZan)
        main_layout.addWidget(self.btnHistory)

        main_layout.addStretch(1)

        self.styleApply()


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
    window = ClientWindow()
    window.show()
    sys.exit(app.exec())