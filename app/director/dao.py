from app.core.dao import BaseDAO
from app.database import db

from datetime import date
from decimal import Decimal
from typing import Any, Dict, List

class DirectorDAO(BaseDAO):
    """DAO для функций директора."""

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