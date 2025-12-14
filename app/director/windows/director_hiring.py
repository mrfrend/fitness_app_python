from __future__ import annotations

from typing import Optional

from PyQt6.QtWidgets import QMainWindow, QWidget

from app.director.interfaces.director_hiring import Ui_MainWindow as UiDirectorHiringWindow


class DirectorHiringWindow(QMainWindow, UiDirectorHiringWindow):
    """Окно найма персонала."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Инициализирует окно найма персонала.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setupUi(self)
