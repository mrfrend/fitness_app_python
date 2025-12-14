from __future__ import annotations

from typing import Optional

from PyQt6.QtWidgets import QMainWindow, QWidget

from app.director.interfaces.director_financial import Ui_MainWindow as UiDirectorFinancialWindow


class DirectorFinancialWindow(QMainWindow, UiDirectorFinancialWindow):
    """Окно финансовых показателей."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Инициализирует окно финансовых показателей.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setupUi(self)
