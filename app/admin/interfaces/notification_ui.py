from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDateEdit,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
import sys


class NotificatioUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Уведомления")


        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)


        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(15)
        main_layout.addLayout(grid_layout)

        self.send_to_text = QLabel("Кому")
        self.send_to_combo = QComboBox()

        self.date_text = QLabel("Дата")
        self.date_enter = QDateEdit(calendarPopup=True)
        self.date_enter.setDisplayFormat("dd.MM.yyyy")
        self.date_enter.setDate(QDate.currentDate())


        self.text_text = QLabel("Текст")
        self.text_enter = QTextEdit("Современные технологии достигли такого уровня, что курс на социально-ориентированный национальный проект требует анализа поставленных обществом задач. Не следует, однако, забывать, что перспективное планирование требует от нас анализа поэтапного и последовательного развития общества.")

        labels = [
            self.send_to_text,
            self.date_text,
            self.text_text
        ]

        values = [self.send_to_combo, self.date_enter, self.text_enter]


        for row, (lbl, val) in enumerate(zip(labels, values)):
            grid_layout.addWidget(lbl, row, 0, alignment=Qt.AlignmentFlag.AlignRight)
            grid_layout.addWidget(val, row, 1)

        btn_layout = QHBoxLayout()
        self.btnSend = QPushButton("Разослать")
        btn_layout.addWidget(self.btnSend)
        self.btnDelete = QPushButton("Удалить")
        btn_layout.addWidget(self.btnDelete)
        main_layout.addLayout(btn_layout)

        btn_layout2 = QHBoxLayout()
        self.btnBack = QPushButton("Назад")
        btn_layout2.addWidget(self.btnBack)
        main_layout.addLayout(btn_layout2)

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
    window = NotificatioUi()
    window.show()
    sys.exit(app.exec())