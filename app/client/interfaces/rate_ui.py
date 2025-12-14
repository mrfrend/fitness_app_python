from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QLineEdit, \
    QPushButton, QDateEdit, QTextEdit

import sys


class RateUi(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Оставить отзыв")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.label = QLabel("Написать отзыв")
        main_layout.addWidget(self.label)


        reason_layout = QHBoxLayout()
        self.labelReason = QLabel("Причина: ")
        reason_layout.addWidget(self.labelReason)
        self.boxReason = QComboBox()
        self.boxReason.addItem("Пожелание")
        self.boxReason.addItem("Жалоба")
        reason_layout.addWidget(self.boxReason)
        main_layout.addLayout(reason_layout)

        date_layout = QHBoxLayout()
        self.labelDate = QLabel("Дата: ")
        date_layout.addWidget(self.labelDate)
        self.dateEdit = QDateEdit()
        date_layout.addWidget(self.dateEdit)
        main_layout.addLayout(date_layout)

        text_layout = QHBoxLayout()
        self.labelText = QLabel("Текст: ")
        text_layout.addWidget(self.labelText)
        self.lineEdit = QTextEdit()
        text_layout.addWidget(self.lineEdit)
        main_layout.addLayout(text_layout)

        btn_layout = QHBoxLayout()
        self.btnSend = QPushButton("Отправить")
        btn_layout.addWidget(self.btnSend)
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
    window = RateUi()
    window.show()
    sys.exit(app.exec())