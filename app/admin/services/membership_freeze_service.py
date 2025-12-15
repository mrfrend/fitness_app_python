from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Dict, List, Optional

from app.admin.db_objects.database_for_me import db


@dataclass(frozen=True)
class FreezeRecord:
    freeze_id: int
    membership_id: int
    client_id: int
    start_date: date
    end_date: date


class MembershipFreezeService:
    STATUS_ACTIVE = "Active"
    STATUS_FROZEN = "Frozen"

    def list_freezes(self) -> List[Dict[str, Any]]:
        with db.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT mf.freezeID,
                       mf.mf_membershipID AS membershipID,
                       m.clientID,
                       mf.startDate,
                       mf.endDate
                FROM MembershipFreezes mf
                JOIN Memberships m ON mf.mf_membershipID = m.membID
                ORDER BY mf.startDate DESC
                """
            )
            return list(cursor.fetchall())

    def save_freeze(self, data: Dict[str, Any]) -> None:
        client_id = int(data["clientID"])
        start_date: date = data["startDate"]
        end_date: date = data["endDate"]

        freeze_id = data.get("freezeID")
        membership_id = data.get("membershipID")

        with db.conn.cursor() as cursor:
            resolved_membership_id = int(membership_id) if membership_id else self._find_membership_for_client(cursor, client_id)
            if not resolved_membership_id:
                raise ValueError("Активный абонемент не найден для клиента")

            status = self._status_for_dates(start_date, end_date)

            if freeze_id:
                cursor.execute(
                    "UPDATE MembershipFreezes SET startDate = %s, endDate = %s WHERE freezeID = %s",
                    (start_date, end_date, freeze_id),
                )
            else:
                cursor.execute(
                    "INSERT INTO MembershipFreezes (mf_membershipID, startDate, endDate) VALUES (%s, %s, %s)",
                    (resolved_membership_id, start_date, end_date),
                )

            cursor.execute(
                "UPDATE Memberships SET membStatus = %s WHERE membID = %s",
                (status, resolved_membership_id),
            )

        db.conn.commit()

    def delete_freeze(self, freeze_id: int, membership_id: Optional[int]) -> None:
        with db.conn.cursor() as cursor:
            cursor.execute("DELETE FROM MembershipFreezes WHERE freezeID = %s", (freeze_id,))
            if membership_id:
                cursor.execute(
                    "UPDATE Memberships SET membStatus = %s WHERE membID = %s",
                    (self.STATUS_ACTIVE, membership_id),
                )

        db.conn.commit()

    def _find_membership_for_client(self, cursor, client_id: int) -> Optional[int]:
        cursor.execute(
            """
            SELECT membID
            FROM Memberships
            WHERE clientID = %s AND membStatus IN (%s, %s)
            ORDER BY endDate DESC
            LIMIT 1
            """,
            (client_id, self.STATUS_ACTIVE, self.STATUS_FROZEN),
        )
        membership = cursor.fetchone()
        if membership:
            return int(membership.get("membID"))

        cursor.execute(
            """
            SELECT membID
            FROM Memberships
            WHERE clientID = %s
            ORDER BY endDate DESC
            LIMIT 1
            """,
            (client_id,),
        )
        membership = cursor.fetchone()
        return int(membership.get("membID")) if membership else None

    def _status_for_dates(self, start: date, end: date) -> str:
        today = date.today()
        if start <= today <= end:
            return self.STATUS_FROZEN
        return self.STATUS_ACTIVE
