from datetime import datetime
from PyQt6.QtWidgets import QMessageBox
from app.client.interfaces.client_ui import ClientWindow as ClientUI
from app.client.dao.client_dao import ClientDAO
from app.client.windows.record_window import RecordWindow
from app.client.windows.myrecord_window import MyRecordWindow
from app.client.windows.history_window import HistoryWindow
from app.client.windows.rate_window import RateWindow


class ClientWindow(ClientUI):
    def __init__(self, client_id):
        super().__init__()
        self.client_id = client_id
        self.dao = ClientDAO()

        # Подключаем обработчики событий
        self.btnZapis.clicked.connect(self.open_record_window)
        self.btnMyZan.clicked.connect(self.open_myrecord_window)
        self.btnHistory.clicked.connect(self.open_history_window)
        self.btnReview.clicked.connect(self.open_rate_window)

        # Загружаем данные клиента
        self.load_client_data()

    def format_date(self, date_obj):
        """Форматирование даты для отображения"""
        if not date_obj:
            return ''

        if hasattr(date_obj, 'strftime'):
            # Если объект имеет метод strftime (datetime.date или datetime.datetime)
            return date_obj.strftime('%d.%m.%Y')
        elif isinstance(date_obj, str):
            # Если это строка
            return date_obj
        else:
            # Для других типов
            return str(date_obj)

    def load_client_data(self):
        """Загрузка данных клиента из БД"""
        try:
            client_data = self.dao.get_client_info(self.client_id)

            if client_data:
                # Устанавливаем данные в поля
                if client_data['full_name']:
                    self.label_name.setText(client_data['full_name'])

                # Убираем поля роста и цели, если их нет в БД
                # Скрываем строку с ростом
                self.label_rost.setVisible(False)
                self.label_height.setVisible(False)
                self.label_height.setText("")

                # Скрываем строку с целью
                self.label_goal.setVisible(False)
                self.label_goal_text.setVisible(False)
                self.label_goal_text.setText("")

                if client_data['birthDate']:
                    try:
                        birth_date = client_data['birthDate']
                        if isinstance(birth_date, str):
                            birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
                        self.dateEdit_birth.setDate(birth_date)
                    except:
                        self.dateEdit_birth.setDate(datetime.now())
                        self.dateEdit_birth.setEnabled(False)  # Делаем недоступным для редактирования
                else:
                    self.dateEdit_birth.setEnabled(False)
                    self.dateEdit_birth.setDate(datetime.now())

                if client_data['email']:
                    self.label_email_text.setText(client_data['email'])
                else:
                    self.label_email_text.setText("Не указан")

                if client_data['phone']:
                    self.label_phone_text.setText(client_data['phone'])
                else:
                    self.label_phone_text.setText("Не указан")

                if client_data['health_limits']:
                    self.label_med_text.setText(client_data['health_limits'])
                else:
                    self.label_med_text.setText("Нет ограничений")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные клиента")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке данных: {str(e)}")

    def open_record_window(self):
        """Открытие окна записи на занятия"""
        self.record_window = RecordWindow(self.client_id, parent=self)
        self.record_window.show()
        self.hide()

    def open_myrecord_window(self):
        """Открытие окна моих записей"""
        self.myrecord_window = MyRecordWindow(self.client_id, parent=self)
        self.myrecord_window.show()
        self.hide()

    def open_history_window(self):
        """Открытие окна истории посещений"""
        self.history_window = HistoryWindow(self.client_id, parent=self)
        self.history_window.show()
        self.hide()

    def open_rate_window(self):
        """Открытие окна отзыва"""
        self.rate_window = RateWindow(self.client_id, parent=self)
        self.rate_window.show()
        self.hide()

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        reply = QMessageBox.question(self, 'Выход',
                                     "Вы уверены, что хотите выйти из личного кабинета?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            from app.client.windows.auth_window import AuthWindow
            self.auth_window = AuthWindow()
            self.auth_window.show()
            event.accept()
        else:
            event.ignore()