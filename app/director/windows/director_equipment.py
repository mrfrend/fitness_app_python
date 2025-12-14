from __future__ import annotations

from typing import Optional

from PyQt6.QtWidgets import QMainWindow, QWidget

from app.director.interfaces.director_equipment import Ui_MainWindow as UiDirectorEquipmentWindow


class DirectorEquipmentWindow(QMainWindow, UiDirectorEquipmentWindow):
    """Окно заявок на закупку оборудования."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Инициализирует окно заявок на закупку оборудования.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setupUi(self)
