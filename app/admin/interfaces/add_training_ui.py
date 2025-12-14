from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QLineEdit, \
    QPushButton, QDateEdit, QGridLayout
from PyQt6.QtCore import Qt
import sys


class AddTrainingUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить занятия")


        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)


        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(15)
        main_layout.addLayout(grid_layout)

        self.type_text = QLabel("Тип")
        self.type_enter = QLabel("Тип")

        self.dateOn_text = QLabel("Дата начала")
        self.dateOn_enter = QLabel("Дата начала")

        self.dateEnd_text = QLabel("Дата конца")
        self.dateEnd_enter = QLabel("Дата конца")

        self.gym_text = QLabel("Зал")
        self.gym_enter = QLabel("Зал")

        self.id_trainer_text = QLabel("тренер")
        self.id_trainer_enter = QLabel("тренер")

        self.max_count_text = QLabel("макс посетителей")
        self.max_count_enter = QLabel("макс посетителей")

        labels = [
            self.type_text, self.dateOn_text, self.dateEnd_text, self.gym_text, self.id_trainer_text, self.max_count_text
            ]

        values = [
            self.type_enter,
            self.dateOn_enter,
            self.dateEnd_enter,
            self.gym_enter,
            self.id_trainer_enter,
            self.max_count_enter
            ]

        for row, (lbl, val) in enumerate(zip(labels, values)):
            grid_layout.addWidget(lbl, row, 0, alignment=Qt.AlignmentFlag.AlignRight)
            grid_layout.addWidget(val, row, 1)

            self.btnSave = QPushButton("Сохранить")
            self.btnBack = QPushButton("Назад")

        main_layout.addWidget(self.btnSave)
        main_layout.addWidget(self.btnBack)

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
    window = AddTrainingUi()
    window.show()
    sys.exit(app.exec())