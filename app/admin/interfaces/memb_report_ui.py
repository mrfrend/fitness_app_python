from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, \
    QPushButton, QTableWidget

import sys


class MembReportUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Отчёты об абонементах")
        self.setFixedSize(520, 400)

        centralwidget = QWidget()
        self.setCentralWidget(centralwidget)
        main_layout = QVBoxLayout()
        centralwidget.setLayout(main_layout)

        self.label = QLabel("Отчёты об абонементах")
        main_layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels(['№', 'id клиента', 'Тип', 'Дата покупки', 'Стоимость'])
        main_layout.addWidget(self.table)


        btn_layout = QHBoxLayout()
        self.btnReport = QPushButton("Составить отчёт")
        btn_layout.addWidget(self.btnReport)
        self.btnExport = QPushButton("Экспорт")
        btn_layout.addWidget(self.btnExport)
        main_layout.addLayout(btn_layout)

        btn_layout2 = QHBoxLayout()
        self.btnDisc = QPushButton("Добавить акцию/скидку")
        btn_layout2.addWidget(self.btnDisc)
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
    window = MembReportUi()
    window.show()
    sys.exit(app.exec())