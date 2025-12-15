from datetime import date

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

from app.admin.interfaces.workload_gym_ui import WorkloadUi
from app.admin.db_objects.database_for_me import db


class WorkloadGymWindow(WorkloadUi):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        self._selected_record = None

        self._setup_table()
        self._setup_connections()
        self._ensure_storage()
        self._load_zones()
        self.load_workloads()

    def _setup_table(self):
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)

    def _setup_connections(self):
        self.table.itemSelectionChanged.connect(self._on_row_selected)
        self.btnAdd.clicked.connect(self._add_record)
        self.btnUpdate.clicked.connect(self._update_record)
        self.btnDelete.clicked.connect(self._delete_record)
        self.btnBack.clicked.connect(self._go_back)

    def _ensure_storage(self):
        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS ZoneWorkloads (
                        workloadID INT NOT NULL AUTO_INCREMENT,
                        zoneID INT NOT NULL,
                        startDate DATE NOT NULL,
                        endDate DATE NOT NULL,
                        description TEXT,
                        PRIMARY KEY (workloadID),
                        CONSTRAINT fk_zoneworkloads_zone
                            FOREIGN KEY (zoneID)
                            REFERENCES Zones(z_zoneID)
                            ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                    """
                )

            db.conn.commit()
        except Exception as exc:
            db.conn.rollback()
            QMessageBox.critical(self, 'Ошибка', f'Не удалось подготовить таблицу: {exc}')

    def _load_zones(self):
        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    "SELECT z_zoneID, zoneName FROM Zones ORDER BY zoneName"
                )
                zones = cursor.fetchall()

            self.zone_select.clear()
            for zone in zones:
                name = zone.get('zoneName', 'Без названия')
                self.zone_select.addItem(f"{name} (ID: {zone.get('z_zoneID')})", zone.get('z_zoneID'))
        except Exception as exc:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить зоны: {exc}')

    def load_workloads(self):
        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT workloadID,
                           zoneID,
                           startDate,
                           endDate,
                           description
                    FROM ZoneWorkloads
                    ORDER BY startDate DESC, workloadID DESC
                    """
                )
                workloads = cursor.fetchall()

            self.table.setRowCount(len(workloads))
            for row, workload in enumerate(workloads):
                workload_id = workload.get('workloadID')
                zone_id = workload.get('zoneID')
                start_date = workload.get('startDate')
                end_date = workload.get('endDate')
                description = workload.get('description', '')

                id_item = QTableWidgetItem(str(workload_id))
                id_item.setData(Qt.ItemDataRole.UserRole, workload)

                self.table.setItem(row, 0, id_item)
                self.table.setItem(row, 1, QTableWidgetItem(self._zone_name(zone_id)))
                self.table.setItem(row, 2, QTableWidgetItem(str(start_date)))
                self.table.setItem(row, 3, QTableWidgetItem(str(end_date)))
                self.table.setItem(row, 4, QTableWidgetItem(description))

            self.table.resizeColumnsToContents()
            self._selected_record = None
        except Exception as exc:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {exc}')

    def _zone_name(self, zone_id):
        for index in range(self.zone_select.count()):
            if self.zone_select.itemData(index) == zone_id:
                return self.zone_select.itemText(index)
        return f"ID: {zone_id}"

    def _on_row_selected(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            self._selected_record = None
            return

        self._selected_record = selected_items[0].data(Qt.ItemDataRole.UserRole)
        record = self._selected_record or {}

        zone_id = record.get('zoneID')
        index = self.zone_select.findData(zone_id)
        if index != -1:
            self.zone_select.setCurrentIndex(index)

        self._set_date(self.start_date, record.get('startDate'))
        self._set_date(self.end_date, record.get('endDate'))
        self.info_input.setPlainText(record.get('description', ''))

    def _set_date(self, widget, value):
        if hasattr(value, 'toPyDate'):
            value = value.toPyDate()
        if isinstance(value, date):
            widget.setDate(value)
            return
        try:
            parts = [int(part) for part in str(value).split('-')]
            if len(parts) == 3:
                widget.setDate(date(parts[0], parts[1], parts[2]))
        except Exception:
            pass

    def _validate_inputs(self):
        if self.zone_select.currentIndex() == -1:
            QMessageBox.warning(self, 'Внимание', 'Выберите зону')
            return None

        start_date = self.start_date.date().toPyDate()
        end_date = self.end_date.date().toPyDate()
        if end_date < start_date:
            QMessageBox.warning(self, 'Внимание', 'Дата окончания должна быть позже даты начала')
            return None

        description = self.info_input.toPlainText().strip()
        if not description:
            QMessageBox.warning(self, 'Внимание', 'Введите описание')
            return None

        return {
            'zoneID': self.zone_select.currentData(),
            'startDate': start_date,
            'endDate': end_date,
            'description': description,
        }

    def _add_record(self):
        data = self._validate_inputs()
        if not data:
            return

        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO ZoneWorkloads (zoneID, startDate, endDate, description)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (data['zoneID'], data['startDate'], data['endDate'], data['description'])
                )

            db.conn.commit()
            QMessageBox.information(self, 'Успех', 'Запись добавлена')
            self.load_workloads()
        except Exception as exc:
            db.conn.rollback()
            QMessageBox.critical(self, 'Ошибка', f'Не удалось добавить запись: {exc}')

    def _update_record(self):
        if not self._selected_record:
            QMessageBox.warning(self, 'Внимание', 'Выберите запись для обновления')
            return

        data = self._validate_inputs()
        if not data:
            return

        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE ZoneWorkloads
                    SET zoneID = %s,
                        startDate = %s,
                        endDate = %s,
                        description = %s
                    WHERE workloadID = %s
                    """,
                    (
                        data['zoneID'],
                        data['startDate'],
                        data['endDate'],
                        data['description'],
                        self._selected_record.get('workloadID')
                    )
                )

            db.conn.commit()
            QMessageBox.information(self, 'Успех', 'Запись обновлена')
            self.load_workloads()
        except Exception as exc:
            db.conn.rollback()
            QMessageBox.critical(self, 'Ошибка', f'Не удалось обновить запись: {exc}')

    def _delete_record(self):
        if not self._selected_record:
            QMessageBox.warning(self, 'Внимание', 'Выберите запись для удаления')
            return

        confirm = QMessageBox.question(
            self,
            'Подтверждение',
            'Удалить выбранную запись?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM ZoneWorkloads WHERE workloadID = %s",
                    (self._selected_record.get('workloadID'),)
                )

            db.conn.commit()
            QMessageBox.information(self, 'Успех', 'Запись удалена')
            self.load_workloads()
        except Exception as exc:
            db.conn.rollback()
            QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить запись: {exc}')

    def _go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()

    def closeEvent(self, event):
        if self.parent_window:
            self.parent_window.show()
        event.accept()
