from __future__ import annotations

import logging
from typing import Optional

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.core.ui_styles import DIRECTOR_UI_STYLESHEET
from app.director.dao import director_dao
from app.director.interfaces.director_equipment import Ui_MainWindow as UiDirectorEquipmentWindow

logger = logging.getLogger(__name__)

_EQUIPMENT_TABLE_COLUMNS = (
    "ID",
    "Наименование",
    "Количество всего",
    "Количество свободно",
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


class DirectorEquipmentWindow(QMainWindow, UiDirectorEquipmentWindow):
    """Окно заявок на закупку оборудования."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Инициализирует окно заявок на закупку оборудования.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Закупка тренажеров")
        self.setStyleSheet(DIRECTOR_UI_STYLESHEET)

        self._equipment_table = QTableWidget(parent=self.centralwidget)
        self._equipment_table.setColumnCount(len(_EQUIPMENT_TABLE_COLUMNS))
        self._equipment_table.setHorizontalHeaderLabels(list(_EQUIPMENT_TABLE_COLUMNS))
        self._equipment_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._equipment_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._equipment_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self._equipment_table.setAlternatingRowColors(True)

        self._button_add = QPushButton("Добавить", parent=self.centralwidget)
        self._button_edit = QPushButton("Редактировать", parent=self.centralwidget)
        self._button_delete = QPushButton("Удалить", parent=self.centralwidget)
        self._button_refresh = QPushButton("Обновить", parent=self.centralwidget)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self._button_add)
        buttons_layout.addWidget(self._button_edit)
        buttons_layout.addWidget(self._button_delete)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self._button_refresh)

        container = QWidget(self.centralwidget)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addLayout(buttons_layout)
        container_layout.addWidget(self._equipment_table)

        self.verticalLayout.insertWidget(1, container)
        self.verticalScrollBar.hide()

        self.pushButton_back.clicked.connect(self._go_back)

        self._button_add.clicked.connect(self._add_equipment)
        self._button_edit.clicked.connect(self._edit_equipment)
        self._button_delete.clicked.connect(self._delete_equipment)
        self._button_refresh.clicked.connect(self._reload_equipment)

        self._reload_equipment()

    def _go_back(self) -> None:
        """Возвращает пользователя в предыдущее окно."""
        parent = self.parent()
        if isinstance(parent, QWidget):
            parent.show()
        self.close()

    def _reload_equipment(self) -> None:
        """Загружает оборудование из БД и отображает в таблице."""
        try:
            rows = director_dao.get_equipment()
            self._equipment_table.setRowCount(len(rows))
            for row_index, row in enumerate(rows):
                equipment_id = int(row.get("equipmentID", 0))
                self._equipment_table.setItem(row_index, 0, QTableWidgetItem(str(equipment_id)))
                self._equipment_table.setItem(row_index, 1, QTableWidgetItem(str(row.get("name_e", ""))))
                self._equipment_table.setItem(row_index, 2, QTableWidgetItem(str(row.get("quantityExist", ""))))
                self._equipment_table.setItem(row_index, 3, QTableWidgetItem(str(row.get("quantityLeft", ""))))

            self._equipment_table.resizeColumnsToContents()
        except Exception as exc:
            logger.exception("Failed to load equipment")
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить оборудование: {exc}")

    def _get_selected_equipment_id(self) -> Optional[int]:
        """Возвращает ID выбранного оборудования."""
        row = self._equipment_table.currentRow()
        if row < 0:
            return None
        item = self._equipment_table.item(row, 0)
        if item is None:
            return None
        try:
            return int(item.text())
        except ValueError:
            return None

    def _open_equipment_dialog(self, title: str, initial: Optional[dict]) -> Optional[dict]:
        """Открывает диалог ввода данных оборудования.

        Args:
            title: Заголовок.
            initial: Начальные данные.

        Returns:
            Данные или None.
        """
        dialog = _EquipmentFormDialog(title=title, initial=initial, parent=self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return None
        return dialog.get_data()

    def _add_equipment(self) -> None:
        """Добавляет оборудование."""
        try:
            payload = self._open_equipment_dialog(title="Добавить оборудование", initial=None)
            if payload is None:
                return

            director_dao.add_equipment(
                name=str(payload["name"]),
                quantity_exist=int(payload["quantity_exist"]),
                quantity_left=int(payload["quantity_left"]),
            )
            QMessageBox.information(self, "Готово", "Оборудование добавлено")
            self._reload_equipment()
        except Exception as exc:
            logger.exception("Failed to add equipment")
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить оборудование: {exc}")

    def _edit_equipment(self) -> None:
        """Редактирует выбранное оборудование."""
        equipment_id = self._get_selected_equipment_id()
        if equipment_id is None:
            QMessageBox.warning(self, "Выбор", "Выберите оборудование в таблице")
            return

        try:
            current = director_dao.get_equipment_by_id(equipment_id=equipment_id)
            if current is None:
                QMessageBox.warning(self, "Ошибка", "Не удалось найти выбранное оборудование")
                return

            payload = self._open_equipment_dialog(title="Редактировать оборудование", initial=current)
            if payload is None:
                return

            updated = director_dao.update_equipment(
                equipment_id=equipment_id,
                name=str(payload["name"]),
                quantity_exist=int(payload["quantity_exist"]),
                quantity_left=int(payload["quantity_left"]),
            )
            if updated == 0:
                QMessageBox.warning(self, "Результат", "Оборудование не найдено")
                return

            QMessageBox.information(self, "Готово", "Оборудование обновлено")
            self._reload_equipment()
        except Exception as exc:
            logger.exception("Failed to edit equipment")
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить оборудование: {exc}")

    def _delete_equipment(self) -> None:
        """Удаляет выбранное оборудование."""
        equipment_id = self._get_selected_equipment_id()
        if equipment_id is None:
            QMessageBox.warning(self, "Выбор", "Выберите оборудование в таблице")
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Удалить оборудование (ID={equipment_id})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            deleted = director_dao.delete_equipment(equipment_id=equipment_id)
            if deleted == 0:
                QMessageBox.warning(self, "Результат", "Оборудование не найдено")
                return
            QMessageBox.information(self, "Готово", "Оборудование удалено")
            self._reload_equipment()
        except Exception as exc:
            logger.exception("Failed to delete equipment")
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить оборудование: {exc}")


class _EquipmentFormDialog(QDialog):
    """Диалог добавления/редактирования оборудования."""

    def __init__(
        self,
        title: str,
        initial: Optional[dict],
        parent: Optional[QWidget] = None,
    ) -> None:
        """Инициализирует диалог.

        Args:
            title: Заголовок.
            initial: Начальные значения.
            parent: Родитель.
        """
        super().__init__(parent)
        self.setWindowTitle(title)

        self._name = QLineEdit(self)
        self._quantity_exist = QLineEdit(self)
        self._quantity_left = QLineEdit(self)

        form = QFormLayout()
        form.addRow("Наименование*", self._name)
        form.addRow("Количество всего*", self._quantity_exist)
        form.addRow("Количество свободно*", self._quantity_left)

        self._buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self._buttons)
        self.setLayout(layout)

        self._apply_initial(initial)

    def _apply_initial(self, initial: Optional[dict]) -> None:
        if not initial:
            self._quantity_left.setText("0")
            return
        self._name.setText(str(initial.get("name_e") or ""))
        self._quantity_exist.setText(str(initial.get("quantityExist") or "0"))
        self._quantity_left.setText(str(initial.get("quantityLeft") or "0"))

    def _validate(self) -> Optional[dict]:
        name = self._name.text().strip()
        if not name:
            QMessageBox.warning(self, "Валидация", "Наименование обязательно")
            return None

        try:
            quantity_exist = int(self._quantity_exist.text().strip())
            quantity_left = int(self._quantity_left.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Валидация", "Количество должно быть целым числом")
            return None

        if quantity_exist < 0 or quantity_left < 0:
            QMessageBox.warning(self, "Валидация", "Количество не может быть отрицательным")
            return None

        if quantity_left > quantity_exist:
            QMessageBox.warning(self, "Валидация", "Свободного не может быть больше, чем всего")
            return None

        return {
            "name": name,
            "quantity_exist": quantity_exist,
            "quantity_left": quantity_left,
        }

    def accept(self) -> None:
        validated = self._validate()
        if validated is None:
            return
        self._result = validated
        super().accept()

    def get_data(self) -> dict:
        """Возвращает данные после принятия."""
        return dict(getattr(self, "_result", {}))
