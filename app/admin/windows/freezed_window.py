from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

from app.admin.interfaces.freezed_ui import FreezedUi
from app.admin.interfaces.addFreeze_ui import AddFreeze
from app.admin.db_objects.database_for_me import db
from app.admin.services.membership_freeze_service import MembershipFreezeService


class FreezedWindow(FreezedUi):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent
        self._selected_freeze = None
        self._freeze_editor = None
        self._freeze_service = MembershipFreezeService()

        self._setup_table()
        self._setup_connections()
        self.load_freezes()

    def _setup_table(self):
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)

    def _setup_connections(self):
        self.table.itemSelectionChanged.connect(self._on_row_selected)
        self.btnAdd.clicked.connect(self._open_add_dialog)
        self.btnEdit.clicked.connect(self._open_edit_dialog)
        self.btnDelete.clicked.connect(self._delete_freeze)
        self.btnBack.clicked.connect(self._go_back)

    def load_freezes(self):
        try:
            freezes = self._freeze_service.list_freezes()

            self.table.setRowCount(len(freezes))
            for row, freeze in enumerate(freezes):
                freeze_id = freeze.get('freezeID')
                start_date = freeze.get('startDate')
                end_date = freeze.get('endDate')

                id_item = QTableWidgetItem(str(freeze_id))
                id_item.setData(Qt.ItemDataRole.UserRole, freeze)

                self.table.setItem(row, 0, id_item)
                self.table.setItem(row, 1, QTableWidgetItem(str(start_date)))
                self.table.setItem(row, 2, QTableWidgetItem(str(end_date)))

            self.table.resizeColumnsToContents()
            self._selected_freeze = None
        except Exception as exc:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить заморозки: {exc}')

    def _on_row_selected(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            self._selected_freeze = None
            return

        freeze_item = selected_items[0]
        self._selected_freeze = freeze_item.data(Qt.ItemDataRole.UserRole)

    def _open_add_dialog(self):
        self._freeze_editor = AddFreeze(parent=self)
        self._freeze_editor.freeze_saved.connect(self._save_freeze)
        self._freeze_editor.back_requested.connect(self._resume_from_dialog)
        self.hide()
        self._freeze_editor.show()

    def _open_edit_dialog(self):
        if not self._selected_freeze:
            QMessageBox.warning(self, 'Внимание', 'Выберите заморозку для редактирования')
            return

        self._freeze_editor = AddFreeze(
            parent=self,
            client_id=self._selected_freeze.get('clientID'),
            freeze=self._selected_freeze,
        )
        self._freeze_editor.freeze_saved.connect(self._save_freeze)
        self._freeze_editor.back_requested.connect(self._resume_from_dialog)
        self.hide()
        self._freeze_editor.show()

    def _save_freeze(self, data):
        try:
            self._freeze_service.save_freeze(data)
            QMessageBox.information(self, 'Успех', 'Заморозка успешно сохранена')
            self.load_freezes()
        except Exception as exc:
            db.conn.rollback()
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить заморозку: {exc}')

    def _delete_freeze(self):
        if not self._selected_freeze:
            QMessageBox.warning(self, 'Внимание', 'Выберите заморозку для удаления')
            return

        freeze_id = self._selected_freeze.get('freezeID')
        confirm = QMessageBox.question(
            self,
            'Подтверждение',
            'Удалить выбранную заморозку?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            self._freeze_service.delete_freeze(
                int(freeze_id),
                int(self._selected_freeze.get('membershipID')) if self._selected_freeze.get('membershipID') else None,
            )
            QMessageBox.information(self, 'Успех', 'Заморозка удалена, абонемент восстановлен')
            self.load_freezes()
        except Exception as exc:
            db.conn.rollback()
            QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить заморозку: {exc}')

    def _resume_from_dialog(self):
        self.show()

    def _go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()

    def closeEvent(self, event):
        if self.parent_window:
            self.parent_window.show()
        event.accept()