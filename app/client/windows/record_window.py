from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from app.client.interfaces.record_ui import RecordUi
from app.client.dao.client_dao import ClientDAO
from datetime import time, timedelta


class RecordWindow(RecordUi):
    def __init__(self, client_id, parent=None):
        super().__init__()
        self.client_id = client_id
        self.parent_window = parent
        self.dao = ClientDAO()
        self.current_classes = []

        # Подключаем обработчики событий
        self.btnRecord.clicked.connect(self.handle_enroll)
        self.btnBack.clicked.connect(self.go_back)
        self.typeEnter.currentTextChanged.connect(self.filter_classes)

        # Загружаем занятия
        self.load_classes()

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

    def load_classes(self):
        """Загрузка списка доступных занятий"""
        try:
            # Получаем все занятия
            self.current_classes = self.dao.get_available_classes(self.client_id)

            # Применяем текущий фильтр
            self.filter_classes(self.typeEnter.currentText())

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке занятий: {str(e)}")

    def filter_classes(self, class_type):
        """Фильтрация занятий по типу (не показываем прошедшие)"""
        try:
            if class_type == "Все":
                filtered_classes = self.current_classes
            elif class_type == "Групповые":
                filtered_classes = [c for c in self.current_classes if c['class_type'] == 'group']
            else:  # "Индивидуальные"
                filtered_classes = [c for c in self.current_classes if c['class_type'] == 'individual']

            # Фильтруем: показываем только доступные и уже записанные (не прошедшие)
            filtered_classes = [c for c in filtered_classes if c.get('availability') != 'past']

            # Очищаем таблицу
            self.table.setRowCount(0)

            # Заполняем таблицу
            for row, class_info in enumerate(filtered_classes):
                self.table.insertRow(row)

                # Добавляем данные в таблицу
                items = [
                    self.format_date(class_info['date']),
                    class_info['name'],
                    self.format_time(class_info['start_time']),
                    self.format_time(class_info['end_time']),
                    class_info.get('hall', ''),
                    str(class_info.get('max_participants', '1')),
                    str(class_info.get('current_participants', '0')),
                    class_info.get('availability', 'unknown')
                ]

                for col, value in enumerate(items):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                    # Цветовая индикация статуса
                    if col == 7:  # Столбец статуса
                        if value == 'enrolled':
                            item.setForeground(Qt.GlobalColor.green)
                            item.setText('Уже записан')
                        elif value == 'full':
                            item.setForeground(Qt.GlobalColor.red)
                            item.setText('Мест нет')
                        elif value == 'occupied':
                            item.setForeground(Qt.GlobalColor.yellow)
                            item.setText('Занято')
                        elif value == 'available':
                            item.setForeground(Qt.GlobalColor.green)
                            item.setText('Доступно')
                        else:
                            item.setForeground(Qt.GlobalColor.white)
                            item.setText(str(value))

                    self.table.setItem(row, col, item)

            # Если после фильтрации нет занятий
            if len(filtered_classes) == 0:
                self.table.setRowCount(1)
                item = QTableWidgetItem("Нет доступных занятий для записи")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(0, 0, item)
                self.table.setSpan(0, 0, 1, 8)  # Объединяем ячейки

            # Настраиваем ширину столбцов
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при фильтрации занятий: {str(e)}")

    def handle_enroll(self):
        """Обработка записи на занятие"""
        # Получаем выбранную строку
        selected_row = self.table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите занятие для записи")
            return

        try:
            # Определяем тип занятия из выбранного фильтра
            filter_type = self.typeEnter.currentText()

            # Получаем ID занятия из фильтрованных данных
            filtered_classes = []
            if filter_type == "Все":
                # Фильтруем прошедшие занятия
                filtered_classes = [c for c in self.current_classes if c.get('availability') != 'past']
            elif filter_type == "Групповые":
                filtered_classes = [c for c in self.current_classes if c['class_type'] == 'group' and c.get('availability') != 'past']
            else:  # "Индивидуальные"
                filtered_classes = [c for c in self.current_classes if c['class_type'] == 'individual' and c.get('availability') != 'past']

            if selected_row >= len(filtered_classes):
                QMessageBox.warning(self, "Ошибка", "Неверный выбор занятия")
                return

            class_info = filtered_classes[selected_row]
            class_id = class_info['id']
            class_type_db = class_info['class_type']

            # Проверяем статус
            availability = class_info.get('availability', 'unknown')
            if availability == 'enrolled':
                QMessageBox.warning(self, "Ошибка", "Вы уже записаны на это занятие")
                return
            elif availability in ['full', 'occupied']:
                QMessageBox.warning(self, "Ошибка", "Нет свободных мест")
                return

            # Подтверждение записи
            reply = QMessageBox.question(
                self, 'Подтверждение записи',
                f"Вы уверены, что хотите записаться на занятие:\n"
                f"\"{class_info['name']}\"\n"
                f"Дата: {self.format_date(class_info['date'])}\n"
                f"Время: {self.format_time(class_info['start_time'])} - {self.format_time(class_info['end_time'])}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Выполняем запись
                success = self.dao.enroll_to_class(self.client_id, class_id, class_type_db)

                if success:
                    QMessageBox.information(self, "Успех", "Вы успешно записались на занятие!")
                    # Обновляем список занятий
                    self.load_classes()
                else:
                    QMessageBox.warning(self, "Ошибка",
                                        "Не удалось записаться на занятие. Возможно, места закончились.")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при записи на занятие: {str(e)}")

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