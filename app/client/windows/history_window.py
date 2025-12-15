from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from app.client.interfaces.history_ui import HistoryUi
from app.client.dao.client_dao import ClientDAO
from app.client.windows.progress_window import ProgressWindow
from datetime import time, timedelta


class HistoryWindow(HistoryUi):
    def __init__(self, client_id, parent=None):
        super().__init__()
        self.client_id = client_id
        self.parent_window = parent
        self.dao = ClientDAO()
        self.history_data = []

        # Подключаем обработчики событий
        self.btnProgress.clicked.connect(self.open_progress)
        self.btnBack.clicked.connect(self.go_back)

        # Загружаем историю
        self.load_history()

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

    def load_history(self):
        """Загрузка истории посещений (показываем прошедшие)"""
        try:
            self.history_data = self.dao.get_client_history(self.client_id)

            # Очищаем таблицу
            self.table.setRowCount(0)

            # Заполняем таблицу
            for row, visit in enumerate(self.history_data):
                self.table.insertRow(row)

                # Добавляем данные в таблицу
                items = [
                    str(visit['id']),
                    self.format_date(visit['date']),
                    self.format_time(visit['time'])
                ]

                for col, value in enumerate(items):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(row, col, item)

            # Если нет истории
            if not self.history_data:
                self.table.setRowCount(1)
                item = QTableWidgetItem("У вас нет истории посещений")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(0, 0, item)
                self.table.setSpan(0, 0, 1, 3)  # Объединяем ячейки

            # Настраиваем ширину столбцов
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке истории: {str(e)}")

    def open_progress(self):
        """Открытие окна прогресса"""
        # Проверяем, выбрана ли запись
        selected_row = self.table.currentRow()

        if selected_row == -1 or not self.history_data:
            QMessageBox.warning(self, "Ошибка", "Выберите посещение для просмотра прогресса")
            return

        try:
            # Получаем информацию о выбранном посещении
            visit = self.history_data[selected_row]
            visit_id = visit['id']

            # Открываем окно прогресса
            self.progress_window = ProgressWindow(self.client_id, visit_id, parent=self)
            self.progress_window.show()
            self.hide()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при открытии прогресса: {str(e)}")

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