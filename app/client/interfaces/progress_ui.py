from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, \
    QTableWidget, QHeaderView, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
import sys


class ProgressUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Прогресс")
        self.setGeometry(100, 100, 700, 400)
        self.setMinimumSize(QSize(700, 400))

        # Основной виджет и layout
        centralwidget = QWidget()
        centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(centralwidget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        centralwidget.setLayout(main_layout)

        # Заголовок с информацией о пользователе
        self.label = QLabel("Прогресс пользователя")
        self.label.setObjectName("titleLabel")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.label)

        # Таблица прогресса
        self.table = QTableWidget()
        self.table.setObjectName("progressTable")
        self.table.setColumnCount(3)  # Изменили с 4 на 3
        self.table.setHorizontalHeaderLabels(['Дата замера', 'Вес', 'Результат'])  # Убрали "Рост"

        # Настройка заголовков таблицы
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        # Устанавливаем стиль для заголовков таблицы
        font = QFont("Segoe UI", 11, QFont.Weight.Bold)
        self.table.horizontalHeader().setFont(font)

        main_layout.addWidget(self.table)

        # Layout для кнопок
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        # Кнопка Назад
        self.btnBack = QPushButton("Назад")
        self.btnBack.setObjectName("btnBack")
        self.btnBack.setMinimumHeight(45)
        self.btnBack.setMinimumWidth(180)

        # Добавляем кнопку в layout с отступами
        btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
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
                margin-bottom: 20px;
            }

            /* Стиль для таблицы */
            QTableWidget#progressTable {
                background-color: #1a1a1a;
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 1px solid #333333;
                border-radius: 8px;
                gridline-color: #333333;
                selection-background-color: #3855c7;
                selection-color: #ffffff;
                alternate-background-color: #252525;
            }

            QTableWidget#progressTable::item {
                padding: 8px;
                border-bottom: 1px solid #333333;
            }

            QTableWidget#progressTable::item:selected {
                background-color: #3855c7;
            }

            /* Стиль для заголовков таблицы */
            QHeaderView::section {
                background-color: #2d2d2d;
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: 600;
                padding: 12px;
                border: none;
                border-right: 1px solid #333333;
                border-bottom: 2px solid #3855c7;
            }

            QHeaderView::section:last {
                border-right: none;
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

        # Дополнительные настройки таблицы
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProgressUi()
    window.show()
    sys.exit(app.exec())