from decimal import Decimal, InvalidOperation

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

from app.admin.interfaces.memb_types_ui import MembTypesUi
from app.admin.db_objects.database_for_me import db


class MembTypesWindow(MembTypesUi):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        self._selected_membership_id = None

        self._setup_table()
        self._setup_connections()
        self.load_memberships()

    def _setup_table(self):
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)

    def _setup_connections(self):
        self.table.itemSelectionChanged.connect(self._on_row_selected)
        self.btnEdit.clicked.connect(self._update_cost)
        self.btnBack.clicked.connect(self._go_back)

    def load_memberships(self):
        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT m.membID,
                           m.membType,
                           m.cost,
                           COALESCE(GROUP_CONCAT(z.zoneName SEPARATOR ', '), 'Без зон') AS zones
                    FROM Memberships m
                    LEFT JOIN MembershipZones mz ON m.membID = mz.mz_membershipID
                    LEFT JOIN Zones z ON mz.mz_zoneID = z.z_zoneID
                    GROUP BY m.membID, m.membType, m.cost
                    ORDER BY m.membType
                    """
                )
                memberships = cursor.fetchall()

            self.table.setRowCount(len(memberships))
            for row, membership in enumerate(memberships):
                membership_id = membership.get('membID')
                memb_type = membership.get('membType', '')
                cost = membership.get('cost', '')
                zones = membership.get('zones', '')

                type_item = QTableWidgetItem(str(memb_type))
                cost_item = QTableWidgetItem(str(cost))
                zones_item = QTableWidgetItem(str(zones))

                type_item.setData(Qt.ItemDataRole.UserRole, membership_id)

                self.table.setItem(row, 0, type_item)
                self.table.setItem(row, 1, cost_item)
                self.table.setItem(row, 2, zones_item)

            self.table.resizeColumnsToContents()
            self.newCostEnter.clear()
            self._selected_membership_id = None
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить абонементы: {str(e)}')

    def _on_row_selected(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            self._selected_membership_id = None
            self.newCostEnter.clear()
            return

        row = selected_items[0].row()
        type_item = self.table.item(row, 0)
        cost_item = self.table.item(row, 1)

        self._selected_membership_id = type_item.data(Qt.ItemDataRole.UserRole)
        self.newCostEnter.setText(cost_item.text())

    def _update_cost(self):
        if not self._selected_membership_id:
            QMessageBox.warning(self, 'Внимание', 'Выберите абонемент для изменения стоимости')
            return

        new_cost_text = self.newCostEnter.text().strip().replace(',', '.')
        if not new_cost_text:
            QMessageBox.warning(self, 'Внимание', 'Введите новую стоимость')
            return

        try:
            new_cost = Decimal(new_cost_text)
        except (InvalidOperation, ValueError):
            QMessageBox.warning(self, 'Ошибка', 'Стоимость должна быть числом')
            return

        if new_cost <= 0:
            QMessageBox.warning(self, 'Ошибка', 'Стоимость должна быть больше нуля')
            return

        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE Memberships SET cost = %s WHERE membID = %s",
                    (str(new_cost), self._selected_membership_id)
                )

            db.conn.commit()
            QMessageBox.information(self, 'Готово', 'Стоимость успешно обновлена')
            self.load_memberships()
        except Exception as e:
            db.conn.rollback()
            QMessageBox.critical(self, 'Ошибка', f'Не удалось обновить стоимость: {str(e)}')

    def _go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()

    def closeEvent(self, event):
        if self.parent_window:
            self.parent_window.show()
        event.accept()
