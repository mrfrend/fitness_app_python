from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from app.client.interfaces.myrecord_ui import MyRecordUi
from app.client.dao.client_dao import ClientDAO
from datetime import time, timedelta


class MyRecordWindow(MyRecordUi):
    def __init__(self, client_id, parent=None):
        super().__init__()
        self.client_id = client_id
        self.parent_window = parent
        self.dao = ClientDAO()
        self.current_enrollments = []

        # Подключаем обработчики событий
        self.btnCancel.clicked.connect(self.handle_cancel)
        self.btnBack.clicked.connect(self.go_back)

        # Загружаем записи
        self.load_enrollments()

    def format_time(self, time_obj):
        """Форматирование времени для отображения"""
        if not time_obj:
            return ''

        if isinstance(time_obj, time):
            # Если это объект datetime.time
            return time_obj.strftime('%H:%M')
        elif isinstance(time_obj, timedelta):
            # Если это timedelta (может приходить из MySQL)
            # Преобразуем timedelta в часы и минуты
            total_seconds = int(time_obj.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours:02d}:{minutes:02d}"
        elif isinstance(time_obj, str):
            # Если это строка
            return time_obj
        else:
            # Для других типов попробуем преобразовать в строку
            return str(time_obj)

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

    def load_enrollments(self):
        """Загрузка активных записей клиента (не показываем прошедшие)"""
        try:
            self.current_enrollments = self.dao.get_client_enrollments(self.client_id)

            # Фильтруем прошедшие занятия
            self.current_enrollments = [e for e in self.current_enrollments if e['time_status'] != 'past']

            # Очищаем таблицу
            self.table.setRowCount(0)

            # Заполняем таблицу
            for row, enrollment in enumerate(self.current_enrollments):
                self.table.insertRow(row)

                # Добавляем данные в таблицу
                items = [
                    str(enrollment['id']),
                    enrollment['trainer_name'],
                    self.format_date(enrollment['date']),
                    self.format_time(enrollment['time']),
                    'Записан' if enrollment['status'] == 'Enrolled' else enrollment['status']
                ]

                for col, value in enumerate(items):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                    # Цветовая индикация статуса
                    if col == 4:  # Столбец статуса
                        if enrollment['status'] == 'Canceled':
                            item.setForeground(Qt.GlobalColor.red)
                        else:
                            item.setForeground(Qt.GlobalColor.green)

                    self.table.setItem(row, col, item)

            # Если нет записей
            if not self.current_enrollments:
                self.table.setRowCount(1)
                item = QTableWidgetItem("У вас нет активных записей")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(0, 0, item)
                self.table.setSpan(0, 0, 1, 5)  # Объединяем ячейки

            # Настраиваем ширину столбцов
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке записей: {str(e)}")

    def handle_cancel(self):
        """Обработка отмены записи"""
        # Получаем выбранную строку
        selected_row = self.table.currentRow()

        if selected_row == -1 or not self.current_enrollments:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для отмены")
            return

        try:
            # Получаем информацию о выбранной записи
            enrollment = self.current_enrollments[selected_row]
            enrollment_id = enrollment['id']
            class_type = enrollment['class_type']

            # Подтверждение отмены
            reply = QMessageBox.question(
                self, 'Подтверждение отмены',
                f"Вы уверены, что хотите отменить запись:\n"
                f"Тренер: {enrollment['trainer_name']}\n"
                f"Дата: {self.format_date(enrollment['date'])}\n"
                f"Время: {self.format_time(enrollment['time'])}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Выполняем отмену
                success = self.dao.cancel_enrollment(enrollment_id, self.client_id, class_type)

                if success:
                    QMessageBox.information(self, "Успех", "Запись успешно отменена!")
                    # Обновляем список записей
                    self.load_enrollments()
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось отменить запись")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при отмене записи: {str(e)}")

    def go_back(self):
        """Возврат к предыдущему окну"""
        if self.parent_window:
            self.parent_window.show()
        self.close()

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        if self.parent_window:
            self.parent_window.show()
        event.accept()