import sys
from PyQt6.QtWidgets import QApplication
from app.client.windows.auth_window import AuthWindow


def main():
    """Точка входа в приложение"""
    app = QApplication(sys.argv)

    # Устанавливаем стиль для всего приложения
    app.setStyleSheet("""
        * {
            font-family: 'Segoe UI', Arial, sans-serif;
        }

        QMessageBox {
            background-color: #1a1a1a;
        }

        QMessageBox QLabel {
            color: #ffffff;
        }

        QMessageBox QPushButton {
            background-color: #3855c7;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            min-width: 80px;
        }

        QMessageBox QPushButton:hover {
            background-color: #2563eb;
        }
    """)

    # Создаем и показываем окно авторизации
    auth_window = AuthWindow()
    auth_window.show()

    # Запускаем главный цикл приложения
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

