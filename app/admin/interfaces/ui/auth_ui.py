from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
import sys


class AuthUi(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Авторизация")
        self.setFixedSize(400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(15)
        central_widget.setLayout(main_layout)


        upper_layout = QHBoxLayout()
        self.label = QLabel("Тип пользователя")
        upper_layout.addWidget(self.label)
        self.typeUser = QComboBox()
        self.typeUser.addItem("Клиент")
        self.typeUser.addItem("Директор")
        self.typeUser.addItem("Тренер")
        self.typeUser.addItem("Администратор")
        upper_layout.addWidget(self.typeUser)
        main_layout.addLayout(upper_layout)


        login_layout = QHBoxLayout()
        self.loginText = QLabel("Логин ")
        login_layout.addWidget(self.loginText)
        self.loginEnter = QLineEdit()
        self.loginEnter.setPlaceholderText("Введите логин")
        login_layout.addWidget(self.loginEnter)
        main_layout.addLayout(login_layout)

        password_layout = QHBoxLayout()
        self.passwordText = QLabel("Пароль ")
        password_layout.addWidget(self.passwordText)
        self.passwordEnter = QLineEdit()
        self.passwordEnter.setPlaceholderText("Введите пароль")
        password_layout.addWidget(self.passwordEnter)
        main_layout.addLayout(password_layout)

        self.loginBtn = QPushButton("Войти")
        main_layout.addWidget(self.loginBtn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.styleApply()

        main_layout.addStretch(1)

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
    window = AuthUi()
    window.show()
    sys.exit(app.exec())