from datetime import date

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

from app.admin.interfaces.schedule_train_ui import ScheduleUi
from app.admin.db_objects.database_for_me import db


class ScheduleTrainWindow(ScheduleUi):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        self._selected_schedule = None

        self._setup_table()
        self._setup_connections()
        self._load_trainers()
        self.load_schedule()

    def _setup_table(self):
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)

    def _setup_connections(self):
        self.table.itemSelectionChanged.connect(self._on_row_selected)
        self.btnAdd.clicked.connect(self._add_schedule)
        self.btnDelete.clicked.connect(self._delete_schedule)
        self.btnBack.clicked.connect(self._go_back)

    def _load_trainers(self):
        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT userID, CONCAT(last_name, ' ', first_name) AS name
                    FROM Users
                    WHERE userType = 'Trainer'
                    ORDER BY last_name
                    """
                )
                trainers = cursor.fetchall()

            self.trainer_select.clear()
            for trainer in trainers:
                display_name = f"{trainer.get('name', 'Без имени')} (ID: {trainer.get('userID')})"
                self.trainer_select.addItem(display_name, trainer.get('userID'))
        except Exception as exc:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить тренеров: {exc}')

    def load_schedule(self):
        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT classID,
                           classDate,
                           className,
                           trainerID
                    FROM GroupClasses
                    ORDER BY classDate DESC, classID DESC
                    """
                )
                schedule = cursor.fetchall()

            self.table.setRowCount(len(schedule))
            for row, entry in enumerate(schedule):
                class_id = entry.get('classID')
                class_date = entry.get('classDate')
                class_name = entry.get('className', '')
                trainer_id = entry.get('trainerID')

                id_item = QTableWidgetItem(str(class_id))
                id_item.setData(Qt.ItemDataRole.UserRole, entry)
                self.table.setItem(row, 0, id_item)
                self.table.setItem(row, 1, QTableWidgetItem(str(class_date)))
                self.table.setItem(row, 2, QTableWidgetItem(class_name))
                self.table.setItem(row, 3, QTableWidgetItem(self._trainer_name(trainer_id)))

            self.table.resizeColumnsToContents()
            self._selected_schedule = None
        except Exception as exc:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить расписание: {exc}')

    def _trainer_name(self, trainer_id):
        for index in range(self.trainer_select.count()):
            if self.trainer_select.itemData(index) == trainer_id:
                return self.trainer_select.itemText(index)
        return f"ID: {trainer_id}"

    def _on_row_selected(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            self._selected_schedule = None
            return

        entry = selected_items[0].data(Qt.ItemDataRole.UserRole)
        self._selected_schedule = entry
        if entry:
            class_date = entry.get('classDate')
            if hasattr(class_date, 'toPyDate'):
                class_date = class_date.toPyDate()
            if isinstance(class_date, date):
                self.date_input.setDate(class_date)
            else:
                try:
                    parts = [int(part) for part in str(class_date).split('-')]
                    if len(parts) == 3:
                        self.date_input.setDate(date(parts[0], parts[1], parts[2]))
                except ValueError:
                    pass

            self.description_input.setPlainText(entry.get('className', ''))
            trainer_id = entry.get('trainerID')
            index = self.trainer_select.findData(trainer_id)
            if index != -1:
                self.trainer_select.setCurrentIndex(index)

    def _add_schedule(self):
        selected_trainer_index = self.trainer_select.currentIndex()
        if selected_trainer_index == -1:
            QMessageBox.warning(self, 'Внимание', 'Выберите тренера')
            return

        class_date = self.date_input.date().toPyDate()
        class_name = self.description_input.toPlainText().strip()
        trainer_id = self.trainer_select.currentData()

        if not class_name:
            QMessageBox.warning(self, 'Внимание', 'Введите описание занятия')
            return

        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO GroupClasses (
                        className,
                        trainerID,
                        classDate,
                        startTime,
                        endTime,
                        hall,
                        maxParticipants,
                        current_participants,
                        classStatus
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        class_name,
                        trainer_id,
                        class_date,
                        '09:00:00',
                        '10:00:00',
                        None,
                        20,
                        0,
                        'Scheduled'
                    )
                )

            db.conn.commit()
            QMessageBox.information(self, 'Успех', 'Занятие добавлено в расписание')
            self.load_schedule()
        except Exception as exc:
            db.conn.rollback()
            QMessageBox.critical(self, 'Ошибка', f'Не удалось добавить занятие: {exc}')

    def _delete_schedule(self):
        if not self._selected_schedule:
            QMessageBox.warning(self, 'Внимание', 'Выберите занятие для удаления')
            return

        response = QMessageBox.question(
            self,
            'Подтверждение',
            'Удалить выбранное занятие?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if response != QMessageBox.StandardButton.Yes:
            return

        class_id = self._selected_schedule.get('classID')

        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM ClassEnrollments WHERE classID = %s",
                    (class_id,)
                )
                cursor.execute(
                    "DELETE FROM GroupClasses WHERE classID = %s",
                    (class_id,)
                )

            db.conn.commit()
            QMessageBox.information(self, 'Успех', 'Занятие удалено')
            self.load_schedule()
        except Exception as exc:
            db.conn.rollback()
            QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить занятие: {exc}')

    def _go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()

    def closeEvent(self, event):
        if self.parent_window:
            self.parent_window.show()
        event.accept()
