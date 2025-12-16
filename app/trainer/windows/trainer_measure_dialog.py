from datetime import date

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QWidget

from app.core.qt import ui_path
from app.core.ui_styles import TRAINER_UI_STYLESHEET
from app.trainer.dao import trainer_dao


class TrainerMeasureDialog(QDialog):
    def __init__(self, client_id: int, parent=None):
        super().__init__(parent)
        uic.loadUi(ui_path("trainer", "interfaces", "trainer_measure.ui"), self)
        self.setStyleSheet(TRAINER_UI_STYLESHEET)
        for child in self.findChildren(QWidget):
            if child is not self and child.styleSheet():
                child.setStyleSheet("")
        self._client_id = client_id
        self._dao = trainer_dao

        self.pushButton_back.clicked.connect(self.reject)
        self.pushButton_save.clicked.connect(self._save)

        self.lineEdit_date.setText(date.today().isoformat())

    def _save(self):
        metric_date = self.lineEdit_date.text().strip()
        raw_weight = self.lineEdit_height.text().strip()
        notes = self.lineEdit_new.text().strip()

        weight = None
        if raw_weight:
            try:
                weight = float(raw_weight.replace(",", "."))
            except ValueError:
                return

        if not metric_date or not notes:
            return

        self._dao.add_client_metric(self._client_id, metric_date=metric_date, notes=notes, weight=weight)
        self.accept()
