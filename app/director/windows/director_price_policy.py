from __future__ import annotations

from typing import Optional

from PyQt6.QtWidgets import QMainWindow, QWidget

from app.director.interfaces.director_price_policy import Ui_MainWindow as UiDirectorPricePolicyWindow


class DirectorPricePolicyWindow(QMainWindow, UiDirectorPricePolicyWindow):
    """Окно управления ценовой политикой."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Инициализирует окно управления ценовой политикой.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setupUi(self)
