from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

from app.admin.interfaces.reports_ui import ReportsUi
from app.admin.db_objects.database_for_me import db


class ReportWindow(ReportsUi):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent

        self._setup_table()
        self._load_complaints()

        if hasattr(self, 'btnBack'):
            self.btnBack.clicked.connect(self._go_back)

    def _setup_table(self):
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)
        self.table.setWordWrap(True)
        self.table.horizontalHeader().setStretchLastSection(True)

    def _load_complaints(self):
        try:
            with db.conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT r.reviewID,
                           r.reviewType,
                           r.dataRev,
                           r.textRev,
                           r.clientID,
                           u.first_name,
                           u.last_name
                    FROM Review r
                    LEFT JOIN Users u ON r.clientID = u.userID
                    ORDER BY r.dataRev DESC, r.reviewID DESC
                    """
                )
                rows = cursor.fetchall()

            self.table.setRowCount(len(rows))
            for row_idx, record in enumerate(rows):
                raw_type = (record.get('reviewType') or '').lower()
                if raw_type in ('suggestion', 'suggestion '):
                    pretty_type = 'Пожелание'
                elif raw_type in ('complaint', 'complain'):
                    pretty_type = 'Жалоба'
                else:
                    pretty_type = 'Отзыв'

                date_value = record.get('dataRev')
                text_value = record.get('textRev', '')
                client_name = f"{record.get('last_name', '')} {record.get('first_name', '')}".strip()

                type_display = pretty_type if not client_name else f"{pretty_type}\n({client_name})"
                type_item = QTableWidgetItem(type_display)
                type_item.setData(Qt.ItemDataRole.UserRole, record)
                date_item = QTableWidgetItem(str(date_value))
                text_item = QTableWidgetItem(text_value)
                text_item.setFlags(text_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                self.table.setItem(row_idx, 0, type_item)
                self.table.setItem(row_idx, 1, date_item)
                self.table.setItem(row_idx, 2, text_item)

            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()
        except Exception as exc:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить отзывы: {exc}')

    def _go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()

    def closeEvent(self, event):
        if self.parent_window:
            self.parent_window.show()
        event.accept()
