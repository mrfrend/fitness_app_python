from __future__ import annotations

import logging
from datetime import date
from typing import Callable, Optional

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.director.dao import director_dao
from app.director.interfaces.director_hiring import Ui_MainWindow as UiDirectorHiringWindow

logger = logging.getLogger(__name__)

_EMPLOYEE_TABLE_COLUMNS = (
    "ID",
    "ФИО",
    "Тип",
    "Телефон",
    "Email",
    "Логин",
    "Дата рождения",
    "Специализации",
)

_EMPLOYEE_TYPES = ("Administrator", "Trainer")

_DEFAULT_EMPLOYEE_HEALTH_LIMITS = "Нет"

_BIRTH_DATE_INPUT_PLACEHOLDER = "YYYY-MM-DD"

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


class DirectorHiringWindow(QMainWindow, UiDirectorHiringWindow):
    """Окно найма персонала."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Инициализирует окно найма персонала.

        Args:
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setupUi(self)

        self._employees_table = QTableWidget(parent=self.centralwidget)
        self._employees_table.setColumnCount(len(_EMPLOYEE_TABLE_COLUMNS))
        self._employees_table.setHorizontalHeaderLabels(list(_EMPLOYEE_TABLE_COLUMNS))
        self._employees_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._employees_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._employees_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self._employees_table.setAlternatingRowColors(True)
        self._employees_table.setStyleSheet(_TABLE_WIDGET_STYLE)
        self.verticalLayout.insertWidget(1, self._employees_table)
        self.verticalScrollBar.hide()

        self.pushButton_back.clicked.connect(self._go_back)
        self.pushButton_add.clicked.connect(self._add_employee)
        self.pushButton_edit.clicked.connect(self._edit_employee)
        self.pushButton_delete.clicked.connect(self._delete_employee)

        self._reload_employees()

    def _open_employee_dialog(
        self,
        title: str,
        is_edit: bool,
        initial: Optional[dict],
        initial_specializations: list[str],
    ) -> Optional[dict]:
        """Открывает единый диалог ввода данных сотрудника.

        Args:
            title: Заголовок окна.
            is_edit: Режим редактирования.
            initial: Начальные данные (для edit).
            initial_specializations: Начальные специализации.

        Returns:
            Словарь с полями сотрудника или None, если отменено.
        """

        dialog = _EmployeeFormDialog(
            title=title,
            is_edit=is_edit,
            initial=initial,
            initial_specializations=initial_specializations,
            date_parser=self._parse_date,
            parent=self,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return None
        return dialog.get_data()

    def _go_back(self) -> None:
        """Возвращает пользователя в предыдущее окно."""
        parent = self.parent()
        if isinstance(parent, QWidget):
            parent.show()
        self.close()

    def _add_employee(self) -> None:
        """Запускает сценарий добавления сотрудника."""
        try:
            payload = self._open_employee_dialog(
                title="Добавить сотрудника",
                is_edit=False,
                initial=None,
                initial_specializations=[],
            )
            if payload is None:
                return

            user_type = str(payload["user_type"])
            specializations = list(payload.get("specializations", []))

            user_id = director_dao.add_employee(
                first_name=str(payload["first_name"]),
                last_name=str(payload["last_name"]),
                middle_name=payload.get("middle_name") or None,
                phone=str(payload["phone"]),
                email=str(payload.get("email", "")),
                login=str(payload["login"]),
                password=str(payload["password"]),
                user_type=user_type,
                birth_date=payload.get("birth_date"),
                health_limits=_DEFAULT_EMPLOYEE_HEALTH_LIMITS,
            )

            if user_type == "Trainer":
                director_dao.set_trainer_specializations(trainer_id=user_id, specializations=specializations)

            QMessageBox.information(self, "Готово", "Сотрудник добавлен")
            self._reload_employees()
        except Exception as exc:
            logger.exception("Failed to add employee")
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить сотрудника: {exc}")

    def _edit_employee(self) -> None:
        """Запускает сценарий редактирования сотрудника."""
        user_id = self._get_selected_user_id()
        if user_id is None:
            QMessageBox.warning(self, "Выбор", "Выберите сотрудника в таблице")
            return

        try:
            employees = director_dao.get_employees()
            current = next((e for e in employees if int(e.get("userID", 0)) == user_id), None)
            if current is None:
                QMessageBox.warning(self, "Ошибка", "Не удалось найти выбранного сотрудника")
                return

            current_specs: list[str] = []
            if str(current.get("userType")) == "Trainer":
                current_specs = director_dao.get_trainer_specializations(trainer_id=user_id)

            payload = self._open_employee_dialog(
                title="Редактировать сотрудника",
                is_edit=True,
                initial=current,
                initial_specializations=current_specs,
            )
            if payload is None:
                return

            user_type = str(payload["user_type"])
            password = payload.get("password")

            director_dao.update_employee(
                user_id=user_id,
                first_name=str(payload["first_name"]),
                last_name=str(payload["last_name"]),
                middle_name=payload.get("middle_name") or None,
                phone=str(payload["phone"]),
                email=str(payload.get("email", "")),
                login=str(payload["login"]),
                password=password,
                user_type=user_type,
                birth_date=payload.get("birth_date"),
                health_limits=_DEFAULT_EMPLOYEE_HEALTH_LIMITS,
            )

            if user_type == "Trainer":
                director_dao.set_trainer_specializations(
                    trainer_id=user_id,
                    specializations=list(payload.get("specializations", [])),
                )
            else:
                director_dao.set_trainer_specializations(trainer_id=user_id, specializations=[])

            QMessageBox.information(self, "Готово", "Данные сотрудника обновлены")
            self._reload_employees()
        except Exception as exc:
            logger.exception("Failed to edit employee")
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить сотрудника: {exc}")

    def _delete_employee(self) -> None:
        """Запускает сценарий удаления сотрудника."""
        user_id = self._get_selected_user_id()
        if user_id is None:
            QMessageBox.warning(self, "Выбор", "Выберите сотрудника в таблице")
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Удалить сотрудника (ID={user_id})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            director_dao.set_trainer_specializations(trainer_id=user_id, specializations=[])
            deleted = director_dao.delete_employee(user_id=user_id)
            if deleted == 0:
                QMessageBox.warning(self, "Результат", "Сотрудник не найден")
                return

            QMessageBox.information(self, "Готово", "Сотрудник удалён")
            self._reload_employees()
        except Exception as exc:
            logger.exception("Failed to delete employee")
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить сотрудника: {exc}")

    def _reload_employees(self) -> None:
        """Загружает сотрудников из БД и отображает в таблице."""
        try:
            employees = director_dao.get_employees()

            self._employees_table.setRowCount(len(employees))
            for row_index, employee in enumerate(employees):
                user_id = int(employee.get("userID", 0))
                fio = " ".join(
                    part
                    for part in (
                        str(employee.get("last_name", "")).strip(),
                        str(employee.get("first_name", "")).strip(),
                        str(employee.get("middle_name") or "").strip(),
                    )
                    if part
                )

                user_type = str(employee.get("userType", ""))
                specs = ""
                if user_type == "Trainer":
                    specs = ", ".join(director_dao.get_trainer_specializations(trainer_id=user_id))

                self._employees_table.setItem(row_index, 0, QTableWidgetItem(str(user_id)))
                self._employees_table.setItem(row_index, 1, QTableWidgetItem(fio))
                self._employees_table.setItem(row_index, 2, QTableWidgetItem(user_type))
                self._employees_table.setItem(row_index, 3, QTableWidgetItem(str(employee.get("phone", ""))))
                self._employees_table.setItem(row_index, 4, QTableWidgetItem(str(employee.get("email", ""))))
                self._employees_table.setItem(row_index, 5, QTableWidgetItem(str(employee.get("login", ""))))
                self._employees_table.setItem(row_index, 6, QTableWidgetItem(str(employee.get("birthDate") or "")))
                self._employees_table.setItem(row_index, 7, QTableWidgetItem(specs))

            self._employees_table.resizeColumnsToContents()
        except Exception as exc:
            logger.exception("Failed to load employees")
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить сотрудников: {exc}")

    def _get_selected_user_id(self) -> Optional[int]:
        """Возвращает ID выбранного сотрудника из таблицы."""
        row = self._employees_table.currentRow()
        if row < 0:
            return None

        item = self._employees_table.item(row, 0)
        if item is None:
            return None

        try:
            return int(item.text())
        except ValueError:
            return None

    def _parse_date(self, value: str) -> Optional[date]:
        """Парсит дату в формате YYYY-MM-DD.

        Args:
            value: Строка даты.

        Returns:
            Объект даты или None, если строка пустая.

        Raises:
            ValueError: Если формат даты некорректный.
        """
        if not value:
            return None

        parts = value.split("-")
        if len(parts) != 3:
            raise ValueError("Invalid date format")

        year, month, day = (int(p) for p in parts)
        return date(year, month, day)


class _EmployeeFormDialog(QDialog):
    """Единый диалог для добавления/редактирования сотрудника."""

    def __init__(
        self,
        title: str,
        is_edit: bool,
        initial: Optional[dict],
        initial_specializations: list[str],
        date_parser: Callable[[str], Optional[date]],
        parent: Optional[QWidget] = None,
    ) -> None:
        """Инициализирует диалог.

        Args:
            title: Заголовок.
            is_edit: True для редактирования.
            initial: Начальные данные сотрудника.
            initial_specializations: Начальные специализации.
            date_parser: Функция парсинга даты.
            parent: Родительский виджет.
        """
        super().__init__(parent)
        self.setWindowTitle(title)
        self._is_edit = is_edit
        self._date_parser = date_parser

        self._user_type = QComboBox(self)
        self._user_type.addItems(list(_EMPLOYEE_TYPES))

        self._last_name = QLineEdit(self)
        self._first_name = QLineEdit(self)
        self._middle_name = QLineEdit(self)
        self._phone = QLineEdit(self)
        self._email = QLineEdit(self)
        self._login = QLineEdit(self)
        self._password = QLineEdit(self)
        self._password.setEchoMode(QLineEdit.EchoMode.Password)
        self._birth_date = QLineEdit(self)
        self._birth_date.setPlaceholderText(_BIRTH_DATE_INPUT_PLACEHOLDER)
        self._specializations = QLineEdit(self)

        form = QFormLayout()
        form.addRow("Тип", self._user_type)
        form.addRow("Фамилия*", self._last_name)
        form.addRow("Имя*", self._first_name)
        form.addRow("Отчество", self._middle_name)
        form.addRow("Телефон*", self._phone)
        form.addRow("Email", self._email)
        form.addRow("Логин*", self._login)
        form.addRow("Пароль", self._password)
        form.addRow("Дата рождения", self._birth_date)
        form.addRow("Специализации", self._specializations)

        self._buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self._buttons)
        self.setLayout(layout)

        self._apply_initial(initial, initial_specializations)
        self._user_type.currentTextChanged.connect(self._sync_specializations_enabled)
        self._sync_specializations_enabled(self._user_type.currentText())

    def _apply_initial(self, initial: Optional[dict], initial_specializations: list[str]) -> None:
        if not initial:
            self._user_type.setCurrentText("Administrator")
            self._password.setPlaceholderText("обязательно")
            return

        self._user_type.setCurrentText(str(initial.get("userType") or "Administrator"))
        self._last_name.setText(str(initial.get("last_name") or ""))
        self._first_name.setText(str(initial.get("first_name") or ""))
        self._middle_name.setText(str(initial.get("middle_name") or ""))
        self._phone.setText(str(initial.get("phone") or ""))
        self._email.setText(str(initial.get("email") or ""))
        self._login.setText(str(initial.get("login") or ""))
        self._password.setPlaceholderText("оставьте пустым, чтобы не менять")
        self._birth_date.setText(str(initial.get("birthDate") or ""))
        self._specializations.setText(", ".join(initial_specializations))

    def _sync_specializations_enabled(self, user_type: str) -> None:
        is_trainer = user_type == "Trainer"
        self._specializations.setEnabled(is_trainer)
        if not is_trainer:
            self._specializations.setText("")

    def _validate(self) -> Optional[dict]:
        user_type = self._user_type.currentText().strip()
        if user_type not in _EMPLOYEE_TYPES:
            QMessageBox.warning(self, "Валидация", "Некорректный тип сотрудника")
            return None

        last_name = self._last_name.text().strip()
        first_name = self._first_name.text().strip()
        phone = self._phone.text().strip()
        login = self._login.text().strip()
        if not last_name or not first_name or not phone or not login:
            QMessageBox.warning(self, "Валидация", "Заполните обязательные поля: фамилия, имя, телефон, логин")
            return None

        password_raw = self._password.text()
        if not self._is_edit and not password_raw:
            QMessageBox.warning(self, "Валидация", "Пароль обязателен при добавлении сотрудника")
            return None

        password: Optional[str]
        if self._is_edit:
            password = password_raw.strip() or None
        else:
            password = password_raw

        birth_raw = self._birth_date.text().strip()
        try:
            birth_date = self._date_parser(birth_raw)
        except ValueError:
            QMessageBox.warning(self, "Валидация", "Дата рождения должна быть в формате YYYY-MM-DD")
            return None

        email = self._email.text().strip()
        if email and "@" not in email:
            QMessageBox.warning(self, "Валидация", "Email должен содержать символ @")
            return None

        specializations: list[str] = []
        if user_type == "Trainer":
            spec_raw = self._specializations.text().strip()
            if spec_raw:
                specializations = [s.strip() for s in spec_raw.split(",") if s.strip()]

        return {
            "user_type": user_type,
            "last_name": last_name,
            "first_name": first_name,
            "middle_name": self._middle_name.text().strip() or None,
            "phone": phone,
            "email": email,
            "login": login,
            "password": password,
            "birth_date": birth_date,
            "specializations": specializations,
        }

    def accept(self) -> None:
        validated = self._validate()
        if validated is None:
            return
        self._result = validated
        super().accept()

    def get_data(self) -> dict:
        """Возвращает данные из диалога после принятия."""
        return dict(getattr(self, "_result", {}))
