from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QWidget

from app.core.navigable_window import NavigableWindow
from app.core.qt import ui_path
from app.core.ui_styles import TRAINER_UI_STYLESHEET
from app.trainer.dao import trainer_dao


class TrainerEquipmentRequestWindow(NavigableWindow):
    def __init__(self, trainer_id: int, parent=None):
        super().__init__(parent_window=parent)
        uic.loadUi(ui_path("trainer", "interfaces", "trainer_req.ui"), self)
        self.setStyleSheet(TRAINER_UI_STYLESHEET)
        for child in self.findChildren(QWidget):
            if child is not self and child.styleSheet():
                child.setStyleSheet("")
        self._trainer_id = trainer_id
        self._dao = trainer_dao

        self.lineEdit_id.setText(str(trainer_id))
        self.pushButton_back.clicked.connect(self._back)
        self.pushButton_ask.clicked.connect(self._ask)

    def _ask(self):
        text = self.lineEdit_write.text().strip()
        if not text:
            return
        message = f"Запрос оборудования от тренера (ID={self._trainer_id}): {text}"
        self._dao.notify_directors(message)
        self.lineEdit_write.setText("")

