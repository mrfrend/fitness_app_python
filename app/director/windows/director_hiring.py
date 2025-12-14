from __future__ import annotations

import logging
from typing import Optional

from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget

from app.director.interfaces.director_hiring import Ui_MainWindow as UiDirectorHiringWindow

logger = logging.getLogger(__name__)


class DirectorHiringWindow(QMainWindow, UiDirectorHiringWindow):
    """Окно найма персонала."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Инициализирует окно найма персонала.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setupUi(self)

        self.pushButton_back.clicked.connect(self._go_back)
        self.pushButton_add.clicked.connect(self._add_employee)
        self.pushButton_edit.clicked.connect(self._edit_employee)
        self.pushButton_delete.clicked.connect(self._delete_employee)

    def _go_back(self) -> None:
        """Возвращает пользователя в предыдущее окно."""
        parent = self.parent()
        if isinstance(parent, QWidget):
            parent.show()
        self.close()

    def _add_employee(self) -> None:
        """Запускает сценарий добавления сотрудника."""
        QMessageBox.information(self, "Найм персонала", "Добавление сотрудника пока не реализовано")

    def _edit_employee(self) -> None:
        """Запускает сценарий редактирования сотрудника."""
        QMessageBox.information(self, "Найм персонала", "Редактирование сотрудника пока не реализовано")

    def _delete_employee(self) -> None:
        """Запускает сценарий удаления сотрудника."""
        QMessageBox.information(self, "Найм персонала", "Удаление сотрудника пока не реализовано")
