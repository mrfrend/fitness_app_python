from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, \
    QPushButton, QTableWidget

import sys


class FreezedUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Замороженные")
        self.setFixedSize(520, 400)

        centralwidget = QWidget()
        self.setCentralWidget(centralwidget)
        main_layout = QVBoxLayout()
        centralwidget.setLayout(main_layout)

        self.label = QLabel("Замороженные")
        main_layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels(['id', 'Дата начала', 'Дата конца'])
        main_layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.btnEdit = QPushButton("Редактировать")
        btn_layout.addWidget(self.btnEdit)
        self.btnAdd = QPushButton("Добавить")
        btn_layout.addWidget(self.btnAdd)
        main_layout.addLayout(btn_layout)

        btn_layout2 = QHBoxLayout()
        self.btnDelete = QPushButton("Удалить")
        btn_layout2.addWidget(self.btnDelete)
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
                        font-size: 20px;
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
    window = FreezedUi()
    window.show()
    sys.exit(app.exec())