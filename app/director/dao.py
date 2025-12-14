from app.core.dao import BaseDAO
from app.database import db

from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Optional, Sequence

_MANAGED_EMPLOYEE_TYPES = ("Administrator", "Trainer")
_MANAGED_EMPLOYEE_TYPES_SQL = ", ".join(["%s"] * len(_MANAGED_EMPLOYEE_TYPES))

class DirectorDAO(BaseDAO):
    """DAO для функций директора."""

    def get_employees(self) -> List[Dict[str, Any]]:
        """Возвращает список сотрудников (все пользователи, кроме клиентов).

        Returns:
            Список сотрудников.
        """
        with self.db.conn.cursor() as cursor:
            cursor.execute(
                "SELECT userID, first_name, last_name, middle_name, phone, email, login, userType, birthDate "
                "FROM Users "
                f"WHERE userType IN ({_MANAGED_EMPLOYEE_TYPES_SQL}) "
                "ORDER BY userType, last_name, first_name",
                _MANAGED_EMPLOYEE_TYPES,
            )
            return list(cursor.fetchall())

    def get_employee_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Возвращает сотрудника по ID.

        Args:
            user_id: ID пользователя.

        Returns:
            Данные сотрудника или None.
        """
        with self.db.conn.cursor() as cursor:
            cursor.execute(
                "SELECT userID, first_name, last_name, middle_name, phone, email, login, userType, birthDate "
                "FROM Users "
                "WHERE userID = %s "
                f"AND userType IN ({_MANAGED_EMPLOYEE_TYPES_SQL})",
                (user_id, *_MANAGED_EMPLOYEE_TYPES),
            )
            return cursor.fetchone()

    def get_memberships(self) -> List[Dict[str, Any]]:
        """Возвращает список абонементов.

        Returns:
            Список абонементов.
        """
        with self.db.conn.cursor() as cursor:
            cursor.execute(
                "SELECT membID, clientID, membType, startDate, endDate, membStatus, cost "
                "FROM Memberships "
                "ORDER BY membID"
            )
            return list(cursor.fetchall())

    def add_employee(
        self,
        first_name: str,
        last_name: str,
        middle_name: Optional[str],
        phone: str,
        email: str,
        login: str,
        password: str,
        user_type: str,
        birth_date: Optional[date],
        health_limits: str,
    ) -> int:
        """Создаёт сотрудника.

        Args:
            first_name: Имя.
            last_name: Фамилия.
            middle_name: Отчество.
            phone: Телефон.
            email: Email.
            login: Логин.
            password: Пароль.
            user_type: Тип пользователя (Director/Administrator/Trainer).
            birth_date: Дата рождения.
            health_limits: Ограничения по здоровью.

        Returns:
            ID созданного пользователя.
        """
        with self.db.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Users "
                "(first_name, last_name, middle_name, phone, email, health_limits, login, password, userType, birthDate) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    first_name,
                    last_name,
                    middle_name,
                    phone,
                    email,
                    health_limits,
                    login,
                    password,
                    user_type,
                    birth_date,
                ),
            )
            self.db.conn.commit()
            return int(cursor.lastrowid)

    def update_employee(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        middle_name: Optional[str],
        phone: str,
        email: str,
        login: str,
        password: Optional[str],
        user_type: str,
        birth_date: Optional[date],
        health_limits: str,
    ) -> int:
        """Обновляет данные сотрудника.

        Args:
            user_id: ID пользователя.
            first_name: Имя.
            last_name: Фамилия.
            middle_name: Отчество.
            phone: Телефон.
            email: Email.
            login: Логин.
            password: Пароль (если None, пароль не меняется).
            user_type: Тип пользователя.
            birth_date: Дата рождения.
            health_limits: Ограничения по здоровью.

        Returns:
            Количество обновлённых строк.
        """
        if password is None:
            with self.db.conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE Users SET "
                    "first_name=%s, last_name=%s, middle_name=%s, phone=%s, email=%s, health_limits=%s, "
                    "login=%s, userType=%s, birthDate=%s "
                    "WHERE userID=%s",
                    (
                        first_name,
                        last_name,
                        middle_name,
                        phone,
                        email,
                        health_limits,
                        login,
                        user_type,
                        birth_date,
                        user_id,
                    ),
                )
                self.db.conn.commit()
                return int(cursor.rowcount)

        with self.db.conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Users SET "
                "first_name=%s, last_name=%s, middle_name=%s, phone=%s, email=%s, health_limits=%s, "
                "login=%s, password=%s, userType=%s, birthDate=%s "
                "WHERE userID=%s",
                (
                    first_name,
                    last_name,
                    middle_name,
                    phone,
                    email,
                    health_limits,
                    login,
                    password,
                    user_type,
                    birth_date,
                    user_id,
                ),
            )
            self.db.conn.commit()
            return int(cursor.rowcount)

    def delete_employee(self, user_id: int) -> int:
        """Удаляет сотрудника.

        Args:
            user_id: ID пользователя.

        Returns:
            Количество удалённых строк (из Users).
        """
        with self.db.conn.cursor() as cursor:
            cursor.execute("DELETE FROM TrainerSpecializations WHERE trainerID = %s", (user_id,))
            cursor.execute("DELETE FROM Users WHERE userID = %s", (user_id,))
            deleted_users = int(cursor.rowcount)
            self.db.conn.commit()
            return deleted_users

    def get_trainer_specializations(self, trainer_id: int) -> List[str]:
        """Возвращает список специализаций тренера.

        Args:
            trainer_id: ID тренера.

        Returns:
            Список специализаций.
        """
        with self.db.conn.cursor() as cursor:
            cursor.execute(
                "SELECT specialization FROM TrainerSpecializations WHERE trainerID = %s ORDER BY specialization",
                (trainer_id,),
            )
            rows = cursor.fetchall()
            return [str(row.get("specialization")) for row in rows]

    def set_trainer_specializations(self, trainer_id: int, specializations: Sequence[str]) -> None:
        """Заменяет список специализаций тренера.

        Args:
            trainer_id: ID тренера.
            specializations: Список специализаций.
        """
        normalized = [str(s).strip() for s in specializations if str(s).strip()]
        with self.db.conn.cursor() as cursor:
            cursor.execute("DELETE FROM TrainerSpecializations WHERE trainerID = %s", (trainer_id,))
            if normalized:
                cursor.executemany(
                    "INSERT INTO TrainerSpecializations (trainerID, specialization) VALUES (%s, %s)",
                    [(trainer_id, spec) for spec in normalized],
                )
            self.db.conn.commit()

    def get_equipment(self) -> List[Dict[str, Any]]:
        """Возвращает список оборудования.

        Returns:
            Список оборудования.
        """
        with self.db.conn.cursor() as cursor:
            cursor.execute(
                "SELECT equipmentID, name_e, quantityExist, quantityLeft "
                "FROM Equipment "
                "ORDER BY equipmentID"
            )
            return list(cursor.fetchall())

    def get_equipment_by_id(self, equipment_id: int) -> Optional[Dict[str, Any]]:
        """Возвращает оборудование по ID.

        Args:
            equipment_id: ID оборудования.

        Returns:
            Данные оборудования или None.
        """
        with self.db.conn.cursor() as cursor:
            cursor.execute(
                "SELECT equipmentID, name_e, quantityExist, quantityLeft "
                "FROM Equipment "
                "WHERE equipmentID = %s",
                (equipment_id,),
            )
            return cursor.fetchone()

    def add_equipment(self, name: str, quantity_exist: int, quantity_left: int) -> int:
        """Добавляет оборудование.

        Args:
            name: Наименование.
            quantity_exist: Количество всего.
            quantity_left: Количество свободно.

        Returns:
            ID созданной записи.
        """
        with self.db.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Equipment (name_e, quantityExist, quantityLeft) VALUES (%s, %s, %s)",
                (name, quantity_exist, quantity_left),
            )
            self.db.conn.commit()
            return int(cursor.lastrowid)

    def update_equipment(self, equipment_id: int, name: str, quantity_exist: int, quantity_left: int) -> int:
        """Обновляет оборудование.

        Args:
            equipment_id: ID оборудования.
            name: Наименование.
            quantity_exist: Количество всего.
            quantity_left: Количество свободно.

        Returns:
            Количество обновлённых строк.
        """
        with self.db.conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Equipment SET name_e=%s, quantityExist=%s, quantityLeft=%s WHERE equipmentID=%s",
                (name, quantity_exist, quantity_left, equipment_id),
            )
            self.db.conn.commit()
            return int(cursor.rowcount)

    def delete_equipment(self, equipment_id: int) -> int:
        """Удаляет оборудование.

        Args:
            equipment_id: ID оборудования.

        Returns:
            Количество удалённых строк.
        """
        with self.db.conn.cursor() as cursor:
            cursor.execute("DELETE FROM Equipment WHERE equipmentID = %s", (equipment_id,))
            self.db.conn.commit()
            return int(cursor.rowcount)

    def get_equipment_inventory_summary(self) -> Dict[str, Any]:
        """Возвращает сводку по инвентарю оборудования.

        Returns:
            Словарь с агрегатами (total_items, total_exist, total_left, total_in_use)
            и списком позиций, где quantityLeft = 0.
        """
        with self.db.conn.cursor() as cursor:
            cursor.execute(
                "SELECT "
                "COUNT(*) AS total_items, "
                "COALESCE(SUM(quantityExist), 0) AS total_exist, "
                "COALESCE(SUM(quantityLeft), 0) AS total_left, "
                "COALESCE(SUM(quantityExist - quantityLeft), 0) AS total_in_use "
                "FROM Equipment"
            )
            totals = cursor.fetchone() or {}

            cursor.execute(
                "SELECT equipmentID, name_e, quantityExist, quantityLeft "
                "FROM Equipment "
                "WHERE quantityLeft = 0 "
                "ORDER BY name_e"
            )
            out_of_stock = list(cursor.fetchall())

            return {
                "total_items": int(totals.get("total_items", 0)),
                "total_exist": int(totals.get("total_exist", 0)),
                "total_left": int(totals.get("total_left", 0)),
                "total_in_use": int(totals.get("total_in_use", 0)),
                "out_of_stock": out_of_stock,
            }

    def update_membership_cost(self, membership_id: int, new_cost: Decimal) -> int:
        """Обновляет стоимость абонемента.

        Args:
            membership_id: ID абонемента.
            new_cost: Новая стоимость.

        Returns:
            Количество обновлённых строк.
        """
        with self.db.conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Memberships SET cost = %s WHERE membID = %s",
                (new_cost, membership_id),
            )
            self.db.conn.commit()
            return int(cursor.rowcount)

    def get_membership_sales_summary(self, date_from: date, date_to: date) -> Dict[str, Any]:
        """Возвращает сводку продаж абонементов за период.

        Args:
            date_from: Дата начала (включительно).
            date_to: Дата окончания (включительно).

        Returns:
            Сводка с количеством продаж и суммой выручки.
        """
        with self.db.conn.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) AS sales_count, COALESCE(SUM(cost), 0) AS total_revenue "
                "FROM Memberships "
                "WHERE startDate BETWEEN %s AND %s",
                (date_from, date_to),
            )
            result = cursor.fetchone() or {}
            return {
                "sales_count": int(result.get("sales_count", 0)),
                "total_revenue": result.get("total_revenue", Decimal("0")),
            }

    def get_visits_summary(self, date_from: date, date_to: date) -> Dict[str, Any]:
        """Возвращает сводку посещений за период.

        Args:
            date_from: Дата начала (включительно).
            date_to: Дата окончания (включительно).

        Returns:
            Сводка с количеством посещений.
        """
        with self.db.conn.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) AS visits_count "
                "FROM Visits "
                "WHERE visitDate BETWEEN %s AND %s",
                (date_from, date_to),
            )
            result = cursor.fetchone() or {}
            return {"visits_count": int(result.get("visits_count", 0))}

director_dao = DirectorDAO(db)