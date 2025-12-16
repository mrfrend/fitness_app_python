from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget

from app.core.ui_styles import TRAINER_UI_STYLESHEET
from app.core.qt import ui_path
from app.trainer.windows.trainer_clients_window import TrainerClientsWindow
from app.trainer.windows.trainer_req_window import TrainerEquipmentRequestWindow
from app.trainer.windows.trainer_schedule_window import TrainerScheduleWindow


class MainTrainerWindow(QMainWindow):
    def __init__(self, trainer_id: int):
        super().__init__()
        uic.loadUi(ui_path("trainer", "interfaces", "main_trainer.ui"), self)
        self.setStyleSheet(TRAINER_UI_STYLESHEET)
        for child in self.findChildren(QWidget):
            if child is not self and child.styleSheet():
                child.setStyleSheet("")
        self._trainer_id = trainer_id

        self.pushButton_schedule.clicked.connect(self._open_schedule)
        self.pushButton_clients.clicked.connect(self._open_clients)
        self.pushButton_equipment.clicked.connect(self._open_equipment)

        self._schedule_window: TrainerScheduleWindow | None = None
        self._clients_window: TrainerClientsWindow | None = None
        self._equipment_window: TrainerEquipmentRequestWindow | None = None

    def _open_schedule(self):
        try:
            if self._schedule_window is None:
                self._schedule_window = TrainerScheduleWindow(self._trainer_id, parent=self)
            self._schedule_window.show()
            self.hide()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть расписание: {e}")
            self.show()

    def _open_clients(self):
        try:
            if self._clients_window is None:
                self._clients_window = TrainerClientsWindow(self._trainer_id, parent=self)
            self._clients_window.show()
            self.hide()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть клиентов: {e}")
            self.show()

    def _open_equipment(self):
        try:
            if self._equipment_window is None:
                self._equipment_window = TrainerEquipmentRequestWindow(self._trainer_id, parent=self)
            self._equipment_window.show()
            self.hide()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть запрос оборудования: {e}")
            self.show()
