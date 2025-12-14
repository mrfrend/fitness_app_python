from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QTableWidget, QTableWidgetItem

from app.core.qt import ui_path
from app.trainer.dao import trainer_dao


class TrainerClassInfoDialog(QDialog):
    def __init__(self, class_id: int, parent=None):
        super().__init__(parent)
        uic.loadUi(ui_path("trainer", "interfaces", "trainer_class_info.ui"), self)
        self._class_id = class_id
        self._dao = trainer_dao

        self._table = QTableWidget(self)
        self._table.setColumnCount(2)
        self._table.setHorizontalHeaderLabels(["Клиент", "Статус"])
        self.verticalLayout.addWidget(self._table)

        self.pushButton_back.clicked.connect(self.reject)
        self.pushButton_save.clicked.connect(self._reload)

        self._reload()

    def _reload(self):
        c = self._dao.get_group_class(self._class_id)
        if c is None:
            self.lineEdit_class.setText(str(self._class_id))
            self.lineEdit_name.setText("")
            self._table.setRowCount(0)
            return

        self.lineEdit_class.setText(str(c["classID"]))
        self.lineEdit_name.setText(str(c["className"]))

        attendance = self._dao.list_group_class_attendance(self._class_id)
        self._table.setRowCount(len(attendance))
        for r, a in enumerate(attendance):
            fio = " ".join(
                [
                    str(a.get("last_name") or ""),
                    str(a.get("first_name") or ""),
                    str(a.get("middle_name") or ""),
                ]
            ).strip()
            self._table.setItem(r, 0, QTableWidgetItem(fio))
            self._table.setItem(r, 1, QTableWidgetItem(str(a.get("status"))))
        self._table.resizeColumnsToContents()
