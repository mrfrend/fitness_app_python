from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QLineEdit, \
    QPushButton, QDateEdit, QGridLayout
from PyQt6.QtCore import Qt
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

        grid_layout1 = QGridLayout()
        grid_layout1.setHorizontalSpacing(20)
        grid_layout1.setVerticalSpacing(15)
        main_layout.addLayout(grid_layout1)

        self.date_text = QLabel("Дата")
        self.date_enter = QDateEdit()

        self.information_text = QLabel("Инфо занятий")
        self.information_enter = QLabel("фо вата фо шнеле")

        grid_layout1.addWidget(self.date_text, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid_layout1.addWidget(self.date_enter, 0, 1)
        grid_layout1.addWidget(self.information_text, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid_layout1.addWidget(self.information_enter, 1, 1)

        self.middle_label = QLabel("Отчет посещаемости:")
        main_layout.addWidget(self.middle_label)

        grid_layout2 = QGridLayout()
        grid_layout2.setHorizontalSpacing(20)
        grid_layout2.setVerticalSpacing(15)
        main_layout.addLayout(grid_layout2)

        self.start_text = QLabel("Начало")
        self.start_enter = QLineEdit()

        self.end_text = QLabel("Конец")
        self.end_enter = QLineEdit()


        grid_layout2.addWidget(self.start_text, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid_layout2.addWidget(self.start_enter, 0, 1)
        grid_layout2.addWidget(self.end_text, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid_layout2.addWidget(self.end_enter, 1, 1)

        btn_layout = QHBoxLayout()
        self.btnCreate = QPushButton("Сформировать отчет")
        self.btnBack = QPushButton("Назад")


        btn_layout.addWidget(self.btnCreate)
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
    window = WorkloadUi()
    window.show()
    sys.exit(app.exec())