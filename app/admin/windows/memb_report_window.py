import os
from decimal import Decimal
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFileDialog,
    QMessageBox,
    QTableWidgetItem,
)

from app.admin.interfaces.memb_report_ui import MembReportUi
from app.admin.interfaces.discount_ui import DiscountUi
from app.admin.db_objects.database_for_me import db


class DiscountWindow(DiscountUi):
    def __init__(self, membership, parent=None):
        super().__init__()
        self.membership = membership
        self.parent_window = parent
        self.selected_discount = None

        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)

        self.btnBack.clicked.connect(self._go_back)
        self.btnAdd.setText('Применить скидку')
        self.btnAdd.clicked.connect(self._apply_discount)
        self.btnEdit.setVisible(False)
        self.btnDelete.setVisible(False)
        self.table.itemSelectionChanged.connect(self._on_discount_selected)

        self._load_discounts()

    def _load_discounts(self):
        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT discountID,
                           percentage_disc,
                           dateStart,
                           dateEnd
                    FROM discount
                    ORDER BY dateStart DESC
                    """
                )
                discounts = cursor.fetchall()

            self.table.setRowCount(len(discounts))
            for row, discount in enumerate(discounts):
                discount_id = discount.get('discountID')
                perc = discount.get('percentage_disc')
                start = discount.get('dateStart')
                end = discount.get('dateEnd')

                id_item = QTableWidgetItem(str(discount_id))
                id_item.setData(Qt.ItemDataRole.UserRole, discount_id)

                self.table.setItem(row, 0, id_item)
                self.table.setItem(row, 1, QTableWidgetItem(f"{perc}%"))
                self.table.setItem(row, 2, QTableWidgetItem(str(start)))
                self.table.setItem(row, 3, QTableWidgetItem(str(end)))

            self.table.resizeColumnsToContents()
        except Exception as exc:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить скидки: {exc}')

    def _on_discount_selected(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            self.selected_discount = None
            return

        row = selected_items[0].row()
        discount_id_item = self.table.item(row, 0)
        percentage_item = self.table.item(row, 1)
        start_item = self.table.item(row, 2)
        end_item = self.table.item(row, 3)

        self.selected_discount = {
            'discountID': discount_id_item.data(Qt.ItemDataRole.UserRole),
            'percentage': percentage_item.text().replace('%', ''),
            'start': start_item.text(),
            'end': end_item.text(),
        }

    def _apply_discount(self):
        if not self.selected_discount:
            QMessageBox.warning(self, 'Внимание', 'Выберите скидку для применения')
            return

        try:
            discount_percentage = Decimal(self.selected_discount['percentage'])
            current_cost = Decimal(str(self.membership.get('cost', '0')))
            discounted_cost = (current_cost * (Decimal('100') - discount_percentage) / Decimal('100')).quantize(Decimal('0.01'))

            with db.conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE Memberships SET discountID = %s, cost = %s WHERE membID = %s",
                    (
                        self.selected_discount['discountID'],
                        str(discounted_cost),
                        self.membership['membID'],
                    ),
                )

            db.conn.commit()

            QMessageBox.information(
                self,
                'Готово',
                (
                    f"Старая стоимость: {current_cost}\n"
                    f"Применена скидка: {discount_percentage}%\n"
                    f"Новая стоимость: {discounted_cost}"
                ),
            )

            if self.parent_window:
                self.parent_window.load_memberships()
                self.parent_window.show()

            self.close()

        except Exception as exc:
            db.conn.rollback()
            QMessageBox.critical(self, 'Ошибка', f'Не удалось применить скидку: {exc}')

    def _go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()

    def closeEvent(self, event):
        if self.parent_window:
            self.parent_window.show()
        event.accept()


class MembReportWindow(MembReportUi):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        self._selected_membership = None
        self._discount_window = None

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
        self.btnDisc.clicked.connect(self._open_discount_window)
        self.btnReport.clicked.connect(self._create_report)
        self.btnExport.clicked.connect(self._export_data)
        self.btnBack.clicked.connect(self._go_back)

    def load_memberships(self):
        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT m.membID,
                           m.clientID,
                           m.membType,
                           m.startDate,
                           m.cost,
                           COALESCE(d.percentage_disc, 0) AS discount
                    FROM Memberships m
                    LEFT JOIN discount d ON m.discountID = d.discountID
                    ORDER BY m.membID
                    """
                )
                memberships = cursor.fetchall()

            self.table.setRowCount(len(memberships))
            for row, membership in enumerate(memberships):
                memb_id = membership.get('membID')
                client_id = membership.get('clientID')
                memb_type = membership.get('membType', '')
                start_date = membership.get('startDate', '')
                cost = membership.get('cost', 0)

                self.table.setItem(row, 0, self._make_item(memb_id))
                self.table.setItem(row, 1, self._make_item(client_id))
                self.table.setItem(row, 2, self._make_item(memb_type))
                self.table.setItem(row, 3, self._make_item(start_date))
                self.table.setItem(row, 4, self._make_item(cost))

            self.table.resizeColumnsToContents()
            self._selected_membership = None
        except Exception as exc:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить абонементы: {exc}')

    def _make_item(self, value):
        item = QTableWidgetItem(str(value))
        item.setData(Qt.ItemDataRole.UserRole, value)
        return item

    def _on_row_selected(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            self._selected_membership = None
            return

        row = selected_items[0].row()
        memb_id_item = self.table.item(row, 0)
        client_id_item = self.table.item(row, 1)
        type_item = self.table.item(row, 2)
        date_item = self.table.item(row, 3)
        cost_item = self.table.item(row, 4)

        self._selected_membership = {
            'membID': memb_id_item.data(Qt.ItemDataRole.UserRole),
            'clientID': client_id_item.data(Qt.ItemDataRole.UserRole),
            'type': type_item.text(),
            'startDate': date_item.text(),
            'cost': cost_item.text(),
        }

    def _open_discount_window(self):
        if not self._selected_membership:
            QMessageBox.warning(self, 'Внимание', 'Выберите абонемент для добавления скидки')
            return

        self._discount_window = DiscountWindow(self._selected_membership, self)
        self.hide()
        self._discount_window.show()

    def _create_report(self):
        try:
            report_lines = ['Отчет по абонементам', '======================', '']
            with db.conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT m.membID,
                           m.clientID,
                           m.membType,
                           m.startDate,
                           m.cost,
                           COALESCE(d.percentage_disc, 0) AS discount,
                           COALESCE(d.dateEnd, 'нет') AS discount_end
                    FROM Memberships m
                    LEFT JOIN discount d ON m.discountID = d.discountID
                    ORDER BY m.membID
                    """
                )
                for membership in cursor.fetchall():
                    report_lines.append(
                        f"№: {membership.get('membID')} | Клиент: {membership.get('clientID')} | "
                        f"Тип: {membership.get('membType')} | Начало: {membership.get('startDate')} | "
                        f"Стоимость: {membership.get('cost')} | Скидка: {membership.get('discount')}% | "
                        f"До: {membership.get('discount_end')}"
                    )

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                'Сохранить отчет',
                os.path.expanduser('~/Отчет по абонементам.txt'),
                'Text Files (*.txt)'
            )

            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(report_lines))
                QMessageBox.information(self, 'Успех', f'Отчет сохранен: {file_path}')

        except Exception as exc:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось создать отчет: {exc}')

    def _export_data(self):
        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT m.membID AS id,
                           m.clientID AS client,
                           m.membType AS type,
                           m.startDate AS start_date,
                           m.cost AS cost,
                           COALESCE(d.percentage_disc, 0) AS discount
                    FROM Memberships m
                    LEFT JOIN discount d ON m.discountID = d.discountID
                    ORDER BY m.membID
                    """
                )
                memberships = cursor.fetchall()

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                'Экспортировать данные',
                os.path.expanduser('~/Абонементы.csv'),
                'CSV Files (*.csv)'
            )

            if not file_path:
                return

            if not file_path.lower().endswith('.csv'):
                file_path += '.csv'

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write('id,client_id,type,start_date,cost,discount\n')
                for membership in memberships:
                    line = ','.join([
                        str(membership.get('id', '')),
                        str(membership.get('client', '')),
                        str(membership.get('type', '')).replace(',', ' '),
                        str(membership.get('start_date', '')),
                        str(membership.get('cost', '')),
                        str(membership.get('discount', '')),
                    ])
                    file.write(line + '\n')

            QMessageBox.information(self, 'Успех', f'Данные экспортированы: {file_path}')

        except Exception as exc:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось экспортировать данные: {exc}')

    def _go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()

    def closeEvent(self, event):
        if self.parent_window:
            self.parent_window.show()
        event.accept()
