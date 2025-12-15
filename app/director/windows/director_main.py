from __future__ import annotations
import sys
import logging
from typing import Optional

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from app.core.ui_styles import DARK_UI_STYLESHEET, DIRECTOR_UI_STYLESHEET
from app.director.interfaces.director_main import Ui_MainWindow as UiDirectorMainWindow
from app.director.windows.director_equipment import DirectorEquipmentWindow
from app.director.windows.director_financial import DirectorFinancialWindow
from app.director.windows.director_hiring import DirectorHiringWindow
from app.director.windows.director_price_policy import DirectorPricePolicyWindow
from app.director.windows.director_statistics import DirectorStatisticsWindow

logger = logging.getLogger(__name__)


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
        self.setWindowTitle("Главное окно директора")
        self.setMinimumHeight(400)
        self.setStyleSheet(DIRECTOR_UI_STYLESHEET)

        self._statistics_window: Optional[DirectorStatisticsWindow] = None
        self._financial_window: Optional[DirectorFinancialWindow] = None
        self._price_policy_window: Optional[DirectorPricePolicyWindow] = None
        self._hiring_window: Optional[DirectorHiringWindow] = None
        self._equipment_window: Optional[DirectorEquipmentWindow] = None

        self.pushButton_statistics.clicked.connect(self._open_statistics)
        self.pushButton_financial.clicked.connect(self._open_financial)
        self.pushButton_price.clicked.connect(self._open_price_policy)
        self.pushButton_hiring.clicked.connect(self._open_hiring)
        self.pushButton_purchase.clicked.connect(self._open_equipment)

    def _open_statistics(self) -> None:
        """Открывает окно общей статистики клуба."""
        try:
            self._statistics_window = DirectorStatisticsWindow(parent=self)
            self.hide()
            self._statistics_window.show()
        except Exception:
            logger.exception("Failed to open statistics window")

    def _open_financial(self) -> None:
        """Открывает окно финансовых показателей."""
        try:
            self._financial_window = DirectorFinancialWindow(parent=self)
            self.hide()
            self._financial_window.show()
        except Exception:
            logger.exception("Failed to open financial window")

    def _open_price_policy(self) -> None:
        """Открывает окно управления ценовой политикой."""
        try:
            self._price_policy_window = DirectorPricePolicyWindow(parent=self)
            self.hide()
            self._price_policy_window.show()
        except Exception:
            logger.exception("Failed to open price policy window")

    def _open_hiring(self) -> None:
        """Открывает окно найма персонала."""
        try:
            self._hiring_window = DirectorHiringWindow(parent=self)
            self.hide()
            self._hiring_window.show()
        except Exception:
            logger.exception("Failed to open hiring window")

    def _open_equipment(self) -> None:
        """Открывает окно заявок на закупку оборудования."""
        try:
            self._equipment_window = DirectorEquipmentWindow(parent=self)
            self.hide()
            self._equipment_window.show()
        except Exception:
            logger.exception("Failed to open equipment window")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_UI_STYLESHEET)
    window = DirectorMainWindow()
    window.show()
    sys.exit(app.exec())