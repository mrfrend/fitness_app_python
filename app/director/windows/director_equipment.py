from __future__ import annotations

import logging
from typing import Optional

from PyQt6.QtWidgets import QMainWindow, QWidget

from app.director.interfaces.director_equipment import Ui_MainWindow as UiDirectorEquipmentWindow

logger = logging.getLogger(__name__)


class DirectorEquipmentWindow(QMainWindow, UiDirectorEquipmentWindow):
    """Окно заявок на закупку оборудования."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Инициализирует окно заявок на закупку оборудования.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setupUi(self)

        self.pushButton_back.clicked.connect(self._go_back)

    def _go_back(self) -> None:
        """Возвращает пользователя в предыдущее окно."""
        parent = self.parent()
        if isinstance(parent, QWidget):
            parent.show()
        self.close()
