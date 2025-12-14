from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication, QMainWindow, QLabel, QHBoxLayout
import sys


class ManageClient(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        client_layout = QHBoxLayout()
        self.label = QLabel("Клиент 1")
        client_layout.addWidget(self.label)
        self.lable2 = QLabel("Статус абонемента")
        client_layout.addWidget(self.lable2)
        main_layout.addLayout(client_layout)

        btn_layout = QHBoxLayout()
        self.btnAdd = QPushButton("Добавить клиента")
        btn_layout.addWidget(self.btnAdd)
        self.btnEdit = QPushButton("Изменить абонемент")
        btn_layout.addWidget(self.btnEdit)
        self.btnBlock = QPushButton("Заблокировать абонемент")
        btn_layout.addWidget(self.btnBlock)
        main_layout.addLayout(btn_layout)

        btn_layout2 = QHBoxLayout()
        self.btnCard = QPushButton("Распечатать клубную карту")
        btn_layout2.addWidget(self.btnCard)
        self.btnFreeze = QPushButton("Заморозить абонемент")
        btn_layout2.addWidget(self.btnFreeze)
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
    window = ManageClient()
    window.show()
    sys.exit(app.exec())