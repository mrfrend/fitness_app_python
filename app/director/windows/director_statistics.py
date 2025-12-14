from __future__ import annotations

from typing import Optional

from PyQt6.QtWidgets import QMainWindow, QWidget

from app.director.interfaces.director_statistics import Ui_MainWindow as UiDirectorStatisticsWindow


class DirectorStatisticsWindow(QMainWindow, UiDirectorStatisticsWindow):
    """Окно общей статистики клуба."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Инициализирует окно общей статистики клуба.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setupUi(self)
