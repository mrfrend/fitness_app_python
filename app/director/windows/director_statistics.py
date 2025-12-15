from __future__ import annotations

import logging
from datetime import date
from typing import Optional

from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget

from app.core.ui_styles import DIRECTOR_UI_STYLESHEET
from app.director.interfaces.director_statistics import Ui_MainWindow as UiDirectorStatisticsWindow
from app.director.dao import director_dao

logger = logging.getLogger(__name__)


class DirectorStatisticsWindow(QMainWindow, UiDirectorStatisticsWindow):
    """Окно общей статистики клуба."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Инициализирует окно общей статистики клуба.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setStyleSheet(DIRECTOR_UI_STYLESHEET)

        self.pushButton_back.clicked.connect(self._go_back)
        self.pushButton_data.clicked.connect(self._generate_report)
        self.dateEdit_from.setCalendarPopup(True)
        self.dateEdit_to.setCalendarPopup(True)

        today = date.today()
        self.dateEdit_from.setDate(today)
        self.dateEdit_to.setDate(today)

    def _go_back(self) -> None:
        """Возвращает пользователя в предыдущее окно."""
        parent = self.parent()
        if isinstance(parent, QWidget):
            parent.show()
        self.close()

    def _generate_report(self) -> None:
        """Формирует отчёт по выбранной статистике."""
        if not self.radioButton_sales.isChecked() and not self.radioButton_visits.isChecked():
            QMessageBox.warning(self, "Валидация", "Выберите тип статистики")
            return

        date_from = self.dateEdit_from.date().toPyDate()
        date_to = self.dateEdit_to.date().toPyDate()
        if date_from > date_to:
            QMessageBox.warning(self, "Валидация", "Дата 'с' не может быть больше даты 'до'")
            return

        try:
            if self.radioButton_sales.isChecked():
                summary = director_dao.get_membership_sales_summary(date_from=date_from, date_to=date_to)
                sales_count = summary.get("sales_count", 0)
                total_revenue = summary.get("total_revenue", 0)
                QMessageBox.information(
                    self,
                    "Отчёт",
                    f"Продажи абонементов за период {date_from} - {date_to}:\n"
                    f"Количество: {sales_count}\n"
                    f"Выручка: {total_revenue}",
                )
                return

            summary = director_dao.get_visits_summary(date_from=date_from, date_to=date_to)
            visits_count = summary.get("visits_count", 0)
            QMessageBox.information(
                self,
                "Отчёт",
                f"Посещения за период {date_from} - {date_to}:\nКоличество: {visits_count}",
            )
        except Exception as exc:
            logger.exception("Failed to generate statistics report")
            QMessageBox.critical(self, "Ошибка", f"Не удалось сформировать отчёт: {exc}")
