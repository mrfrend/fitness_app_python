from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from app.client.interfaces.progress_ui import ProgressUi
from app.client.dao.client_dao import ClientDAO
from datetime import timedelta


class ProgressWindow(ProgressUi):
    def __init__(self, client_id, visit_id=None, parent=None):
        super().__init__()
        self.client_id = client_id
        self.visit_id = visit_id
        self.parent_window = parent
        self.dao = ClientDAO()

        # Подключаем обработчики событий
        self.btnBack.clicked.connect(self.go_back)

        # Загружаем прогресс
        self.load_progress()

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

    def load_progress(self):
        """Загрузка метрик прогресса"""
        try:
            # Получаем прогресс клиента
            progress_data = self.dao.get_progress_metrics(self.client_id)

            # Очищаем таблицу
            self.table.setRowCount(0)

            # Заполняем таблицу (теперь только 3 колонки)
            for row, metric in enumerate(progress_data):
                self.table.insertRow(row)

                # Добавляем данные в таблицу (убрали рост)
                items = [
                    self.format_date(metric['measurement_date']),
                    str(metric['weight']) if metric['weight'] else '—',
                    metric['result'] if metric['result'] else '—'
                ]

                for col, value in enumerate(items):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(row, col, item)

            # Если нет данных о прогрессе
            if not progress_data:
                self.table.setRowCount(1)
                item = QTableWidgetItem("Нет данных о прогрессе")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(0, 0, item)
                self.table.setSpan(0, 0, 1, 3)  # Объединяем ячейки (теперь 3 колонки)

            # Обновляем заголовок с информацией о клиенте
            client_info = self.dao.get_client_info(self.client_id)
            if client_info and client_info['full_name']:
                self.label.setText(f"Прогресс: {client_info['full_name']}")

            # Настраиваем ширину столбцов
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке прогресса: {str(e)}")

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