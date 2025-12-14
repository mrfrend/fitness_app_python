from __future__ import annotations

from typing import Optional

from PyQt6.QtWidgets import QMainWindow, QWidget

from app.director.interfaces.director_main import Ui_MainWindow as UiDirectorMainWindow


class DirectorMainWindow(QMainWindow, UiDirectorMainWindow):
    """Главное окно директора.

    Attributes:
        parent: Родительский виджет.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Инициализирует главное окно директора.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setupUi(self)
