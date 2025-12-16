from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem

from app.core.navigable_window import NavigableWindow
from app.core.qt import ui_path
from app.trainer.dao import trainer_dao
from app.trainer.windows.trainer_measure_dialog import TrainerMeasureDialog
from app.trainer.windows.trainer_rec_dialog import TrainerRecommendationDialog


class TrainerClientsWindow(NavigableWindow):
    def __init__(self, trainer_id: int, parent=None):
        super().__init__(parent_window=parent)
        uic.loadUi(ui_path("trainer", "interfaces", "trainer_clients.ui"), self)
        self._trainer_id = trainer_id
        self._dao = trainer_dao

        self._table = QTableWidget(self)
        self._table.setColumnCount(4)
        self._table.setHorizontalHeaderLabels(["ID", "ФИО", "Телефон", "Ограничения"])
        self.verticalLayout.addWidget(self._table)

        self.pushButton_back.clicked.connect(self._back)
        self.pushButton_fix.clicked.connect(self._open_measure)
        self.pushButton_rec.clicked.connect(self._open_recommendation)
        self.lineEdit_client.textChanged.connect(self._apply_filter)

        self._clients: list[dict] = []
        self._reload()

    def _reload(self):
        self._clients = self._dao.list_my_clients(self._trainer_id)
        self._render(self._clients)

    def _apply_filter(self):
        raw = self.lineEdit_client.text().strip()
        if not raw:
            self._render(self._clients)
            return
        if not raw.isdigit():
            self._render([])
            return
        client_id = int(raw)
        filtered = [c for c in self._clients if int(c["userID"]) == client_id]
        self._render(filtered)

    def _render(self, rows: list[dict]):
        self._table.setRowCount(len(rows))
        for r, c in enumerate(rows):
            fio = " ".join(
                [
                    str(c.get("last_name") or ""),
                    str(c.get("first_name") or ""),
                    str(c.get("middle_name") or ""),
                ]
            ).strip()
            self._table.setItem(r, 0, QTableWidgetItem(str(c.get("userID"))))
            self._table.setItem(r, 1, QTableWidgetItem(fio))
            self._table.setItem(r, 2, QTableWidgetItem(str(c.get("phone") or "")))
            self._table.setItem(r, 3, QTableWidgetItem(str(c.get("health_limits") or "")))
        self._table.resizeColumnsToContents()

    def _selected_client_id(self) -> int | None:
        raw = self.lineEdit_client.text().strip()
        if raw.isdigit():
            return int(raw)
        items = self._table.selectedItems()
        if not items:
            return None
        try:
            return int(items[0].text())
        except ValueError:
            return None

    def _open_measure(self):
        client_id = self._selected_client_id()
        if client_id is None:
            return
        dlg = TrainerMeasureDialog(client_id, self)
        dlg.exec()

    def _open_recommendation(self):
        client_id = self._selected_client_id()
        if client_id is None:
            return
        dlg = TrainerRecommendationDialog(self._trainer_id, client_id, self)
        dlg.exec()

