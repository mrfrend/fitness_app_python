from __future__ import annotations

import logging
from decimal import Decimal
from typing import Optional

from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QWidget

from app.core.ui_styles import DIRECTOR_UI_STYLESHEET
from app.director.interfaces.director_price_policy import Ui_MainWindow as UiDirectorPricePolicyWindow
from app.director.dao import director_dao

logger = logging.getLogger(__name__)

_MEMBERSHIP_TABLE_COLUMNS = (
    "ID",
    "Тип",
    "Цена",
    "Статус",
    "Начало",
    "Окончание",
    "Клиент",
)

_TABLE_WIDGET_STYLE = (
    "QTableWidget {"
    "  background-color: #111111;"
    "  color: #FFFFFF;"
    "  gridline-color: #444444;"
    "}"
    "QHeaderView::section {"
    "  background-color: #222222;"
    "  color: #FFFFFF;"
    "  padding: 4px;"
    "  border: 1px solid #333333;"
    "}"
    "QTableWidget::item:selected {"
    "  background-color: #3854C7;"
    "  color: #FFFFFF;"
    "}"
    "QTableWidget::item:alternate {"
    "  background-color: #1A1A1A;"
    "}"
)


class DirectorPricePolicyWindow(QMainWindow, UiDirectorPricePolicyWindow):
    """Окно управления ценовой политикой."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Инициализирует окно управления ценовой политикой.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Ценовая политика")
        self.setStyleSheet(DIRECTOR_UI_STYLESHEET)

        self._memberships_table = QTableWidget(parent=self.centralwidget)
        self._memberships_table.setColumnCount(len(_MEMBERSHIP_TABLE_COLUMNS))
        self._memberships_table.setHorizontalHeaderLabels(list(_MEMBERSHIP_TABLE_COLUMNS))
        self._memberships_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._memberships_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._memberships_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self._memberships_table.setAlternatingRowColors(True)
        self.verticalLayout.insertWidget(0, self._memberships_table)
        self.verticalScrollBar.hide()

        self._memberships_table.itemSelectionChanged.connect(self._apply_selected_membership)

        self.pushButton_update_data.clicked.connect(self._reload_memberships)
        self.pushButton_save_data.clicked.connect(self._save_price)
        self.pushButton_back.clicked.connect(self._go_back)

        self._reload_memberships()

    def _apply_selected_membership(self) -> None:
        row = self._memberships_table.currentRow()
        if row < 0:
            return

        membership_id_item = self._memberships_table.item(row, 0)
        price_item = self._memberships_table.item(row, 2)

        membership_id_text = membership_id_item.text().strip() if membership_id_item is not None else ""
        price_text = price_item.text().strip() if price_item is not None else ""

        self.lineEdit_id.setText(membership_id_text)
        self.lineEdit_new_price.setText(price_text)

    def _go_back(self) -> None:
        """Возвращает пользователя в предыдущее окно."""
        parent = self.parent()
        if isinstance(parent, QWidget):
            parent.show()
        self.close()

    def _reload_memberships(self) -> None:
        """Загружает список абонементов из БД и отображает его в таблице."""
        try:
            memberships = director_dao.get_memberships()
            self._memberships_table.setRowCount(len(memberships))

            for row_index, membership in enumerate(memberships):
                self._memberships_table.setItem(
                    row_index,
                    0,
                    QTableWidgetItem(str(membership.get("membID", ""))),
                )
                self._memberships_table.setItem(
                    row_index,
                    1,
                    QTableWidgetItem(str(membership.get("membType", ""))),
                )
                self._memberships_table.setItem(
                    row_index,
                    2,
                    QTableWidgetItem(str(membership.get("cost", ""))),
                )
                self._memberships_table.setItem(
                    row_index,
                    3,
                    QTableWidgetItem(str(membership.get("membStatus", ""))),
                )
                self._memberships_table.setItem(
                    row_index,
                    4,
                    QTableWidgetItem(str(membership.get("startDate", ""))),
                )
                self._memberships_table.setItem(
                    row_index,
                    5,
                    QTableWidgetItem(str(membership.get("endDate", ""))),
                )
                self._memberships_table.setItem(
                    row_index,
                    6,
                    QTableWidgetItem(str(membership.get("clientID", ""))),
                )

            self._memberships_table.resizeColumnsToContents()
        except Exception as exc:
            logger.exception("Failed to load memberships")
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить абонементы: {exc}")

    def _save_price(self) -> None:
        """Сохраняет новую цену абонемента в БД."""
        membership_id_raw = self.lineEdit_id.text().strip()
        new_price_raw = self.lineEdit_new_price.text().strip().replace(",", ".")

        if not membership_id_raw or not new_price_raw:
            QMessageBox.warning(self, "Валидация", "Заполните ID абонемента и новую цену")
            return

        try:
            membership_id = int(membership_id_raw)
        except ValueError:
            QMessageBox.warning(self, "Валидация", "ID абонемента должен быть числом")
            return

        try:
            new_price = Decimal(new_price_raw)
        except Exception:
            QMessageBox.warning(self, "Валидация", "Новая цена должна быть числом")
            return

        if new_price <= 0:
            QMessageBox.warning(self, "Валидация", "Новая цена должна быть больше 0")
            return

        try:
            updated = director_dao.update_membership_cost(membership_id=membership_id, new_cost=new_price)
            if updated == 0:
                QMessageBox.warning(self, "Результат", "Абонемент с таким ID не найден")
                return

            QMessageBox.information(self, "Готово", "Цена успешно обновлена")
            self._reload_memberships()
        except Exception as exc:
            logger.exception("Failed to update membership cost")
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить цену: {exc}")
