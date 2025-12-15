from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QLineEdit, QPushButton, QTableWidget
import sys


class MyRecordUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мои записи")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)


        self.label = QLabel("Мои записи")
        main_layout.addWidget(self.label)

        btn_layout = QHBoxLayout()
        self.btnCancel = QPushButton("Отменить")
        btn_layout.addWidget(self.btnCancel)
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
    window = MyRecordUi()
    window.show()
    sys.exit(app.exec())
