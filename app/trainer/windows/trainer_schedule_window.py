from PyQt6 import uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem, QWidget

from app.core.navigable_window import NavigableWindow
from app.core.qt import ui_path
from app.core.ui_styles import TRAINER_UI_STYLESHEET
from app.trainer.dao import trainer_dao
from app.trainer.windows.trainer_class_info_dialog import TrainerClassInfoDialog


class TrainerScheduleWindow(NavigableWindow):
    def __init__(self, trainer_id: int, parent=None):
        super().__init__(parent_window=parent)
        uic.loadUi(ui_path("trainer", "interfaces", "trainer_schedule.ui"), self)
        self.setStyleSheet(TRAINER_UI_STYLESHEET)
        for child in self.findChildren(QWidget):
            if child is not self and child.styleSheet():
                child.setStyleSheet("")
        self._trainer_id = trainer_id
        self._dao = trainer_dao

        self._table = QTableWidget(self)
        self._table.setColumnCount(7)
        self._table.setHorizontalHeaderLabels(
            ["Тип", "ID", "Название/Цель", "Дата", "Начало", "Конец", "Статус"]
        )
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self._table.setAlternatingRowColors(True)
        self.verticalLayout.addWidget(self._table)

        self.comboBox_type.currentIndexChanged.connect(self._reload)
        self._table.cellDoubleClicked.connect(self._open_info)
        self.pushButton_back.clicked.connect(self._back)
        self.pushButton_check.clicked.connect(self._mark_busy)
        self.pushButton_data.clicked.connect(self._swap_shift)

        today = QDate.currentDate()
        self.dateEdit_from.setDate(today)
        self.dateEdit_to.setDate(today)

        self._reload()

    def _mark_busy(self):
        date_from = self.dateEdit_from.date().toString("yyyy-MM-dd")
        date_to = self.dateEdit_to.date().toString("yyyy-MM-dd")
        if not date_from or not date_to:
            return

        if self.dateEdit_to.date() < self.dateEdit_from.date():
            QMessageBox.warning(self, "Занятость", "Дата 'до' не может быть раньше даты 'с'.")
            return

        try:
            self._dao.add_trainer_busy(self._trainer_id, date_from=date_from, date_to=date_to, note=None)
            QMessageBox.information(self, "Занятость", "Период занятости сохранён.")
            self._reload()
        except Exception as e:
            QMessageBox.critical(self, "Занятость", f"Не удалось сохранить занятость: {e}")

    def _swap_shift(self):
        raw_trainer = self.lineEdit_trainer.text().strip()
        raw_entity = self.lineEdit_label.text().strip()

        if not raw_trainer.isdigit():
            QMessageBox.warning(self, "Обмен сменами", "Введите корректный ID тренера.")
            return
        to_trainer_id = int(raw_trainer)
        if to_trainer_id == self._trainer_id:
            QMessageBox.warning(self, "Обмен сменами", "Нельзя обменяться сменой с самим собой.")
            return
        if not self._dao.trainer_exists(to_trainer_id):
            QMessageBox.warning(self, "Обмен сменами", f"Тренер с ID={to_trainer_id} не найден.")
            return

        entity_id: int | None = None
        kind: str | None = None
        if raw_entity.isdigit():
            entity_id = int(raw_entity)
            selected = self.comboBox_type.currentText().strip().lower()
            kind = "Group" if selected == "групповые" else "Personal"
        else:
            items = self._table.selectedItems()
            if items:
                try:
                    row = items[0].row()
                    kind = self._table.item(row, 0).text()
                    entity_id = int(self._table.item(row, 1).text())
                except Exception:
                    entity_id = None

        if entity_id is None or kind not in ("Group", "Personal"):
            QMessageBox.warning(self, "Обмен сменами", "Выберите занятие в таблице или введите ID занятия.")
            return

        try:
            if kind == "Group":
                changed = self._dao.swap_group_class_trainer(entity_id, self._trainer_id, to_trainer_id)
            else:
                changed = self._dao.swap_personal_training_trainer(entity_id, self._trainer_id, to_trainer_id)

            if changed <= 0:
                QMessageBox.warning(
                    self,
                    "Обмен сменами",
                    "Не удалось изменить тренера для занятия. Проверьте ID и что занятие принадлежит вам.",
                )
                return

            QMessageBox.information(self, "Обмен сменами", "Смена успешно изменена.")
            self.lineEdit_label.setText("")
            self._reload()
        except Exception as e:
            QMessageBox.critical(self, "Обмен сменами", f"Не удалось выполнить обмен сменами: {e}")

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

        try:
            for b in self._dao.list_trainer_busy(self._trainer_id):
                date_from = str(b.get("dateFrom"))
                date_to = str(b.get("dateTo"))
                note = str(b.get("note") or "")
                label = note if note else "Busy"
                rows.append(
                    (
                        "Busy",
                        b.get("busyID"),
                        label,
                        f"{date_from}..{date_to}",
                        "",
                        "",
                        "Busy",
                    )
                )
        except Exception:
            pass

        self._table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                self._table.setItem(r, c, QTableWidgetItem(str(value)))
        self._table.resizeColumnsToContents()

    def _open_info(self, row: int, _col: int):
        kind = self._table.item(row, 0).text()
        if kind != "Group":
            return
        try:
            entity_id = int(self._table.item(row, 1).text())
        except Exception:
            return
        dlg = TrainerClassInfoDialog(entity_id, self)
        dlg.exec()

