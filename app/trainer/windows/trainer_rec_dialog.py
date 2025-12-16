from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QWidget

from app.core.qt import ui_path
from app.core.ui_styles import TRAINER_UI_STYLESHEET
from app.trainer.dao import trainer_dao


class TrainerRecommendationDialog(QDialog):
    def __init__(self, trainer_id: int, client_id: int, parent=None):
        super().__init__(parent)
        uic.loadUi(ui_path("trainer", "interfaces", "trainer_rec.ui"), self)
        self.setStyleSheet(TRAINER_UI_STYLESHEET)
        for child in self.findChildren(QWidget):
            if child is not self and child.styleSheet():
                child.setStyleSheet("")
        self._trainer_id = trainer_id
        self._client_id = client_id
        self._dao = trainer_dao

        self.pushButton_back.clicked.connect(self.reject)
        self.pushButton_save.clicked.connect(self._save)

    def _save(self):
        text = self.lineEdit_write.text().strip()
        if not text:
            return

        message = f"Рекомендация от тренера (ID={self._trainer_id}): {text}"
        self._dao.notify_user(self._client_id, message)
        self.accept()
