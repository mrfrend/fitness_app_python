from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem

from app.core.navigable_window import NavigableWindow
from app.core.qt import ui_path
from app.trainer.dao import trainer_dao
from app.trainer.windows.trainer_class_info_dialog import TrainerClassInfoDialog


class TrainerScheduleWindow(NavigableWindow):
    def __init__(self, trainer_id: int, parent=None):
        super().__init__(parent_window=parent)
        uic.loadUi(ui_path("trainer", "interfaces", "trainer_schedule.ui"), self)
        self._trainer_id = trainer_id
        self._dao = trainer_dao

        self._table = QTableWidget(self)
        self._table.setColumnCount(7)
        self._table.setHorizontalHeaderLabels(
            ["Тип", "ID", "Название/Цель", "Дата", "Начало", "Конец", "Статус"]
        )
        self.verticalLayout.addWidget(self._table)

        self.comboBox_type.currentIndexChanged.connect(self._reload)
        self._table.cellDoubleClicked.connect(self._open_info)
        self.pushButton_back.clicked.connect(self._back)
        self.pushButton_check.clicked.connect(self._mark_busy)
        self.pushButton_data.clicked.connect(self._swap_shift)

        self._reload()

    def _mark_busy(self):
        QMessageBox.information(self, "Занятость", "Функция отметки занятости пока не реализована.")

    def _swap_shift(self):
        QMessageBox.information(self, "Обмен сменами", "Функция обмена сменами пока не реализована.")

    def _reload(self):
        selected = self.comboBox_type.currentText().strip().lower()
        rows = []

        if selected == "групповые":
            for c in self._dao.list_group_classes_for_trainer(self._trainer_id):
                rows.append(
                    (
                        "Group",
                        c["classID"],
                        c["className"],
                        str(c["classDate"]),
                        str(c["startTime"]),
                        str(c["endTime"]),
                        c["classStatus"],
                    )
                )
        else:
            for t in self._dao.list_personal_trainings_for_trainer(self._trainer_id):
                rows.append(
                    (
                        "Personal",
                        t["trainingID"],
                        t["goalTraining"],
                        str(t["trainingDate"]),
                        str(t["startTime"]),
                        str(t["endTime"]),
                        "Scheduled",
                    )
                )

        self._table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                self._table.setItem(r, c, QTableWidgetItem(str(value)))
        self._table.resizeColumnsToContents()

    def _open_info(self, row: int, _col: int):
        kind = self._table.item(row, 0).text()
        entity_id = int(self._table.item(row, 1).text())
        if kind != "Group":
            return
        dlg = TrainerClassInfoDialog(entity_id, self)
        dlg.exec()

