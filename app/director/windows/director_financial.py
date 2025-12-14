from __future__ import annotations

import logging
from datetime import date
from typing import Optional

from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget

from app.director.interfaces.director_financial import Ui_MainWindow as UiDirectorFinancialWindow
from app.director.dao import director_dao

logger = logging.getLogger(__name__)

_ALL_TIME_START_DATE = date(1900, 1, 1)


class DirectorFinancialWindow(QMainWindow, UiDirectorFinancialWindow):
    """Окно финансовых показателей."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Инициализирует окно финансовых показателей.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setupUi(self)

        self.pushButton_back.clicked.connect(self._go_back)
        self.pushButton_data.clicked.connect(self._generate_report)
        self.pushButton_strat_data.clicked.connect(self._generate_strategic_report)

    def _go_back(self) -> None:
        """Возвращает пользователя в предыдущее окно."""
        parent = self.parent()
        if isinstance(parent, QWidget):
            parent.show()
        self.close()

    def _generate_report(self) -> None:
        """Формирует отчёт по выбранному финансовому показателю."""
        if not self.radioButton_tiskets.isChecked() and not self.radioButton_purchases.isChecked():
            QMessageBox.warning(self, "Валидация", "Выберите показатель")
            return

        if self.radioButton_purchases.isChecked():
            try:
                summary = director_dao.get_equipment_inventory_summary()
                out_of_stock = summary.get("out_of_stock", [])
                out_of_stock_lines = "\n".join(
                    f"- {row.get('name_e')} (ID={row.get('equipmentID')})" for row in out_of_stock
                )
                if not out_of_stock_lines:
                    out_of_stock_lines = "Нет"

                QMessageBox.information(
                    self,
                    "Отчёт",
                    "Инвентарь оборудования (текущее состояние):\n"
                    f"Позиции: {summary.get('total_items', 0)}\n"
                    f"Всего единиц: {summary.get('total_exist', 0)}\n"
                    f"Свободно: {summary.get('total_left', 0)}\n"
                    f"Занято/используется: {summary.get('total_in_use', 0)}\n\n"
                    "Требуют внимания (quantityLeft = 0):\n"
                    f"{out_of_stock_lines}",
                )
            except Exception as exc:
                logger.exception("Failed to generate equipment inventory report")
                QMessageBox.critical(self, "Ошибка", f"Не удалось сформировать отчёт по оборудованию: {exc}")
            return

        try:
            today = date.today()
            summary = director_dao.get_membership_sales_summary(
                date_from=_ALL_TIME_START_DATE,
                date_to=today,
            )
            QMessageBox.information(
                self,
                "Отчёт",
                "Продажи абонементов (всё время):\n"
                f"Количество: {summary.get('sales_count', 0)}\n"
                f"Выручка: {summary.get('total_revenue', 0)}",
            )
        except Exception as exc:
            logger.exception("Failed to generate financial report")
            QMessageBox.critical(self, "Ошибка", f"Не удалось сформировать отчёт: {exc}")

    def _generate_strategic_report(self) -> None:
        """Формирует стратегический отчёт (сводка по продажам и посещениям)."""
        try:
            today = date.today()
            sales = director_dao.get_membership_sales_summary(
                date_from=_ALL_TIME_START_DATE,
                date_to=today,
            )
            visits = director_dao.get_visits_summary(
                date_from=_ALL_TIME_START_DATE,
                date_to=today,
            )

            equipment = director_dao.get_equipment_inventory_summary()

            QMessageBox.information(
                self,
                "Стратегический отчёт",
                "Сводка (всё время):\n"
                f"Продажи абонементов: {sales.get('sales_count', 0)}\n"
                f"Выручка: {sales.get('total_revenue', 0)}\n"
                f"Посещения: {visits.get('visits_count', 0)}\n\n"
                "Оборудование (текущее состояние):\n"
                f"Позиции: {equipment.get('total_items', 0)}\n"
                f"Всего единиц: {equipment.get('total_exist', 0)}\n"
                f"Свободно: {equipment.get('total_left', 0)}\n"
                f"Занято/используется: {equipment.get('total_in_use', 0)}",
            )
        except Exception as exc:
            logger.exception("Failed to generate strategic financial report")
            QMessageBox.critical(self, "Ошибка", f"Не удалось сформировать стратегический отчёт: {exc}")
