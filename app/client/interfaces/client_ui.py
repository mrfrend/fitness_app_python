from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QDateEdit, QPushButton, \
    QGridLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, QSize
import sys


class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пользователь")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(QSize(700, 500))

        # Основной виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        central_widget.setLayout(main_layout)

        # GridLayout для информации о пользователе
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setVerticalSpacing(20)

        # Создаем метки и поля для данных
        # ФИО
        self.label_fio = QLabel("ФИО:")
        self.label_name = QLabel("Иванов Сергей Петрович")

        # Рост
        self.label_rost = QLabel("Рост:")
        self.label_height = QLabel("190")

        # Дата рождения
        self.label_birth = QLabel("Дата рождения:")
        self.dateEdit_birth = QDateEdit()
        self.dateEdit_birth.setCalendarPopup(True)

        # Цель занятий
        self.label_goal = QLabel("Цель занятий:")
        self.label_goal_text = QLabel("Мышцы хочу")

        # Email
        self.label_email = QLabel("Email:")
        self.label_email_text = QLabel("ivanovsergay190@mail.ru")

        # Телефон
        self.label_phone = QLabel("Телефон:")
        self.label_phone_text = QLabel("89261726312")

        # Медицинские ограничения
        self.label_med = QLabel("Мед. ограничения:")
        self.label_med_text = QLabel("Нет")

        # Добавляем элементы в grid layout
        grid_layout.addWidget(self.label_fio, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid_layout.addWidget(self.label_name, 0, 1)

        grid_layout.addWidget(self.label_rost, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid_layout.addWidget(self.label_height, 1, 1)

        grid_layout.addWidget(self.label_birth, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid_layout.addWidget(self.dateEdit_birth, 2, 1)

        grid_layout.addWidget(self.label_goal, 3, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid_layout.addWidget(self.label_goal_text, 3, 1)

        grid_layout.addWidget(self.label_email, 4, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid_layout.addWidget(self.label_email_text, 4, 1)

        grid_layout.addWidget(self.label_phone, 5, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid_layout.addWidget(self.label_phone_text, 5, 1)

        grid_layout.addWidget(self.label_med, 6, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid_layout.addWidget(self.label_med_text, 6, 1)

        main_layout.addLayout(grid_layout)

        # Кнопки
        self.btnZapis = QPushButton("Запись на занятие")
        self.btnZapis.setMinimumHeight(45)

        self.btnMyZan = QPushButton("Мои занятия")
        self.btnMyZan.setMinimumHeight(45)

        self.btnHistory = QPushButton("История посещений")
        self.btnHistory.setMinimumHeight(45)

        self.btnReview = QPushButton("Написать отзыв")
        self.btnReview.setMinimumHeight(45)

        main_layout.addWidget(self.btnZapis)
        main_layout.addWidget(self.btnMyZan)
        main_layout.addWidget(self.btnHistory)
        main_layout.addWidget(self.btnReview)

        # Растягивающийся спейсер
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(spacer)

        # Применяем стили
        self.styleApply()

    def styleApply(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
            }

            QWidget#centralwidget {
                background-color: #000000;
            }

            /* Стиль для заголовков (ФИО:, Рост: и т.д.) */
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 16px;
            }

            /* Дополнительный стиль для заголовков (жирный текст) */
            QLabel[label_fio],
            QLabel[label_rost],
            QLabel[label_birth],
            QLabel[label_goal],
            QLabel[label_email],
            QLabel[label_phone],
            QLabel[label_med] {
                font-weight: 500;
            }

            /* Стиль для полей с данными */
            QLabel[label_name],
            QLabel[label_height],
            QLabel[label_goal_text],
            QLabel[label_email_text],
            QLabel[label_phone_text],
            QLabel[label_med_text] {
                font-weight: normal;
            }

            /* Стиль для QDateEdit */
            QDateEdit {
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 15px;
                background-color: #333333;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 8px;
                min-height: 35px;
            }

            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #555555;
            }

            QDateEdit::down-arrow {
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid #ffffff;
            }

            /* Стиль для кнопок */
            QPushButton {
                background-color: #3855c7;
                color: white;
                font-family: 'Segoe UI';
                font-size: 16px;
                font-weight: 600;
                border: none;
                border-radius: 8px;
                padding: 12px;
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