from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QTableWidget
import sys

class ScheduleUi(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(['Дата', 'Описание'])
        main_layout.addWidget(self.table)

        trainer_layout = QHBoxLayout()
        self.idTrainer = QLabel("id Тренера")
        trainer_layout.addWidget(self.idTrainer)
        self.idTrainerEnter = QLineEdit()
        trainer_layout.addWidget(self.idTrainerEnter)
        main_layout.addLayout(trainer_layout)
        self.btn1 = QPushButton("Назначить")
        main_layout.addWidget(self.btn1)

        btn_layout = QHBoxLayout()
        self.btnAdd = QPushButton("Добавить занятие")
        btn_layout.addWidget(self.btnAdd)
        self.btnDelete = QPushButton("Удалить занятие")
        btn_layout.addWidget(self.btnDelete)
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
    window = ScheduleUi()
    window.show()
    sys.exit(app.exec())
