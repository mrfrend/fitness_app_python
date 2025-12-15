import sys
from PyQt6.QtWidgets import QMessageBox
from app.client.interfaces.auth_ui import AuthUi
from app.client.dao.client_dao import ClientDAO
from app.client.windows.client_window import ClientWindow


class AuthWindow(AuthUi):
    def __init__(self):
        super().__init__()
        self.dao = ClientDAO()

        # Подключаем обработчики событий
        self.loginBtn.clicked.connect(self.handle_login)
        self.passwordEnter.returnPressed.connect(self.handle_login)

        # Устанавливаем стиль для авторизации
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }

            QWidget {
                background-color: #1a1a1a;
            }

            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 14px;
            }

            QComboBox {
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 14px;
                background-color: #333333;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 8px;
            }

            QLineEdit {
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 14px;
                background-color: #333333;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 8px;
            }

            QPushButton {
                background-color: #3855c7;
                color: white;
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: 600;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                min-width: 100px;
            }

            QPushButton:hover {
                background-color: #2563eb;
            }

            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)

    def handle_login(self):
        """Обработка авторизации"""
        login = self.loginEnter.text().strip()
        password = self.passwordEnter.text().strip()
        user_type = self.typeUser.currentText()

        # Определяем тип пользователя для БД
        type_mapping = {
            'Клиент': 'Client',
            'Директор': 'Director',
            'Тренер': 'Trainer',
            'Администратор': 'Administrator'
        }

        db_user_type = type_mapping.get(user_type)

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        # Проверяем авторизацию
        user = self.dao.authenticate_user(login, password, db_user_type)

        if user:
            # Пока только для клиентов
            if db_user_type == 'Client':
                # Открываем главное окно клиента
                self.client_window = ClientWindow(user['userID'])
                self.client_window.show()
                self.hide()
            else:
                QMessageBox.information(self, "Информация",
                                        f"Добро пожаловать, {user['first_name']}!\n"
                                        f"Интерфейс для {user_type.lower()} в разработке.")
        else:
            QMessageBox.warning(self, "Ошибка",
                                "Неверный логин, пароль или тип пользователя")

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        reply = QMessageBox.question(self, 'Подтверждение',
                                     "Вы уверены, что хотите выйти?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
            sys.exit(0)
        else:
            event.ignore()