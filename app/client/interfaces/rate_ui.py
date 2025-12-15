from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, \
    QPushButton, QDateEdit, QTextEdit, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
import sys


class RateUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оставить отзыв")
        self.setGeometry(100, 100, 700, 600)
        self.setMinimumSize(QSize(700, 600))

        # Основной виджет и layout
        central_widget = QWidget()
        central_widget.setObjectName("centralwidget")
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        central_widget.setLayout(main_layout)

        # Заголовок
        self.label = QLabel("Написать отзыв")
        self.label.setObjectName("titleLabel")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.label)

        # Причина отзыва
        reason_layout = QHBoxLayout()
        reason_layout.setSpacing(15)

        self.labelReason = QLabel("Причина:")
        self.labelReason.setObjectName("fieldLabel")
        self.labelReason.setMinimumWidth(100)

        self.boxReason = QComboBox()
        self.boxReason.setObjectName("reasonComboBox")
        self.boxReason.setMinimumHeight(40)
        self.boxReason.addItem("Пожелание")
        self.boxReason.addItem("Жалоба")

        reason_layout.addWidget(self.labelReason)
        reason_layout.addWidget(self.boxReason)
        reason_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        main_layout.addLayout(reason_layout)

        # Дата
        date_layout = QHBoxLayout()
        date_layout.setSpacing(15)

        self.labelDate = QLabel("Дата:")
        self.labelDate.setObjectName("fieldLabel")
        self.labelDate.setMinimumWidth(100)

        self.dateEdit = QDateEdit()
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setMinimumHeight(40)
        self.dateEdit.setCalendarPopup(True)

        date_layout.addWidget(self.labelDate)
        date_layout.addWidget(self.dateEdit)
        date_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        main_layout.addLayout(date_layout)

        # Текст отзыва
        text_layout = QVBoxLayout()
        text_layout.setSpacing(10)

        self.labelText = QLabel("Текст отзыва:")
        self.labelText.setObjectName("fieldLabel")

        self.textEdit = QTextEdit()
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setMinimumHeight(150)
        self.textEdit.setPlaceholderText("Введите ваш отзыв здесь...")

        text_layout.addWidget(self.labelText)
        text_layout.addWidget(self.textEdit)

        main_layout.addLayout(text_layout)

        # Layout для кнопок
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        # Кнопки
        self.btnSend = QPushButton("Отправить")
        self.btnSend.setObjectName("btnSend")
        self.btnSend.setMinimumHeight(45)
        self.btnSend.setMinimumWidth(180)

        self.btnBack = QPushButton("Назад")
        self.btnBack.setObjectName("btnBack")
        self.btnBack.setMinimumHeight(45)
        self.btnBack.setMinimumWidth(180)

        # Добавляем кнопки в layout
        btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        btn_layout.addWidget(self.btnSend)
        btn_layout.addWidget(self.btnBack)
        btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        main_layout.addLayout(btn_layout)

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

            /* Стиль для заголовка */
            QLabel#titleLabel {
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 24px;
                font-weight: 600;
                padding: 10px;
                margin-bottom: 10px;
            }

            /* Стиль для меток полей */
            QLabel#fieldLabel {
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 16px;
                font-weight: 500;
            }

            /* Стиль для выпадающего списка */
            QComboBox#reasonComboBox {
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 15px;
                background-color: #333333;
                border: 1px solid #555555;
                border-radius: 8px;
                padding: 8px 15px;
                min-height: 40px;
            }

            QComboBox#reasonComboBox::drop-down {
                border: 0;
                width: 30px;
            }

            QComboBox#reasonComboBox::down-arrow {
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid #ffffff;
            }

            QComboBox#reasonComboBox QAbstractItemView {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 8px;
                padding: 5px;
                selection-background-color: #3855c7;
            }

            /* Стиль для поля даты */
            QDateEdit#dateEdit {
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 15px;
                background-color: #333333;
                border: 1px solid #555555;
                border-radius: 8px;
                padding: 8px 15px;
                min-height: 40px;
            }

            QDateEdit#dateEdit::drop-down {
                border: 0;
                width: 30px;
            }

            QDateEdit#dateEdit::down-arrow {
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid #ffffff;
            }

            /* Стиль для текстового поля */
            QTextEdit#textEdit {
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 15px;
                background-color: #333333;
                border: 1px solid #555555;
                border-radius: 8px;
                padding: 12px;
            }

            QTextEdit#textEdit::placeholder {
                color: #888888;
                font-style: italic;
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
                padding: 12px 24px;
                min-width: 180px;
            }

            QPushButton:hover {
                background-color: #2563eb;
            }

            QPushButton:pressed {
                background-color: #1d4ed8;
            }

            /* Стиль для кнопки Назад */
            QPushButton#btnBack {
                background-color: #444444;
            }

            QPushButton#btnBack:hover {
                background-color: #555555;
            }

            QPushButton#btnBack:pressed {
                background-color: #333333;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RateUi()
    window.show()
    sys.exit(app.exec())