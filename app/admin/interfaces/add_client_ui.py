from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QLineEdit, \
    QPushButton, QDateEdit, QGridLayout
from PyQt6.QtCore import Qt
import sys


class AddClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить клиента")


        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)


        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(15)
        main_layout.addLayout(grid_layout)

        self.f_text = QLabel("Фaмилия")
        self.f_enter = QLabel("Иванов")

        self.i_text = QLabel("Имя")
        self.i_enter = QLabel("Сергей")

        self.o_text = QLabel("Отчество")
        self.o_enter = QLabel("Петрович")

        self.birth_text = QLabel("Дата рождения:")
        self.birth_enter = QDateEdit()

        self.goal_text = QLabel("Цель занятий:")
        self.goal_enter = QLabel("Мышцы хочу")

        self.rost_text = QLabel("Рост:")
        self.rost_enter = QLabel("190")

        self.email_text = QLabel("Email:")
        self.email_enter = QLabel("ivanovsergay190@mail.ru")

        self.phone_text = QLabel("Телефон:")
        self.phone_enter = QLabel("89261726312")

        self.med_text = QLabel("Мед. ограничения:")
        self.med_enter = QLabel("Нет")

        labels = [
            self.f_text, self.i_text, self.o_text, self.rost_text, self.birth_text,
            self.goal_text, self.email_text, self.phone_text, self.med_text
        ]

        values = [
            self.f_enter, self.i_enter, self.o_enter, self.rost_enter, self.birth_enter,
            self.goal_enter, self.email_enter, self.phone_enter, self.med_enter
        ]

        for row, (lbl, val) in enumerate(zip(labels, values)):
            grid_layout.addWidget(lbl, row, 0, alignment=Qt.AlignmentFlag.AlignRight)
            grid_layout.addWidget(val, row, 1)


        self.btnCreate = QPushButton("Создать")
        self.btnBack = QPushButton("Назад")

        main_layout.addWidget(self.btnCreate)
        main_layout.addWidget(self.btnBack)

        main_layout.addStretch(1)



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
    window = AddClientWindow()
    window.show()
    sys.exit(app.exec())