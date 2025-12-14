from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QLineEdit, QPushButton, QTableWidget
import sys

class RecordUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Запись")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setMinimumSize(800, 400)

        self.label = QLabel("Запись на занятия")
        main_layout.addWidget(self.label)

        type_layout = QHBoxLayout()
        self.typeText = QLabel("Тип: ")
        type_layout.addWidget(self.typeText)
        self.typeEnter = QComboBox()
        self.typeEnter.addItem("Групповые")
        self.typeEnter.addItem("Индивидуальные")
        type_layout.addWidget(self.typeEnter)
        main_layout.addLayout(type_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(8)

        self.table.setHorizontalHeaderLabels(['Дата', 'Название', 'Начало', 'Конец', 'Зал', 'Макс. кол-во чел.', 'Уже записано', 'Статус'])
        main_layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.btnRecord = QPushButton("Записаться")
        btn_layout.addWidget(self.btnRecord)
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
                            font-size: 20px;
                            color: #fff;
                        }

                        QComboBox, QLineEdit {
                            padding: 6px;
                            border: 1px solid #aaa;
                            border-radius: 6px;
                        }

                        QComboBox::drop-down {
                            border: 0;
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
    window = RecordUi()
    window.show()
    sys.exit(app.exec())