from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, \
    QPushButton, QTableWidget

import sys


class HistoryUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("История")

        centralwidget = QWidget()
        self.setCentralWidget(centralwidget)
        main_layout = QVBoxLayout()
        centralwidget.setLayout(main_layout)

        self.label = QLabel("История посещений")
        main_layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels(['id', 'Дата', 'Время'])
        main_layout.addWidget(self.table)


        btn_layout = QHBoxLayout()
        self.btnProgress = QPushButton("Посмотреть прогресс")
        btn_layout.addWidget(self.btnProgress)
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
    window = HistoryUi()
    window.show()
    sys.exit(app.exec())