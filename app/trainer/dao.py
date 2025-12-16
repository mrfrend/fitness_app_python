from app.core.dao import BaseDAO
from app.database import Database
from app.database import db


class TrainerDAO(BaseDAO):
    def __init__(self, db: Database):
        super().__init__(db)

    def _ensure_trainer_busy_table(self) -> None:
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS TrainerBusy (
                busyID INT NOT NULL AUTO_INCREMENT,
                trainerID INT NOT NULL,
                dateFrom DATE NOT NULL,
                dateTo DATE NOT NULL,
                note VARCHAR(250) DEFAULT NULL,
                PRIMARY KEY (busyID),
                KEY trainerID (trainerID),
                CONSTRAINT trainerbusy_ibfk_1 FOREIGN KEY (trainerID) REFERENCES Users (userID)
            )
            """
        )
        self.commit()

    def get_trainer(self, trainer_id: int):
        return self.fetch_one(
            """
            SELECT userID, first_name, last_name, middle_name, phone, email, health_limits, userType, birthDate
            FROM Users
            WHERE userID = %s AND userType = 'Trainer'
            """,
            (trainer_id,),
        )

    def trainer_exists(self, trainer_id: int) -> bool:
        val = self.fetch_scalar(
            """
            SELECT 1
            FROM Users
            WHERE userID = %s AND userType = 'Trainer'
            """,
            (trainer_id,),
        )
        return val is not None

    def swap_group_class_trainer(self, class_id: int, from_trainer_id: int, to_trainer_id: int) -> int:
        rowcount = self.execute(
            """
            UPDATE GroupClasses
            SET trainerID = %s
            WHERE classID = %s AND trainerID = %s
            """,
            (to_trainer_id, class_id, from_trainer_id),
        )
        self.commit()
        return rowcount

    def swap_personal_training_trainer(self, training_id: int, from_trainer_id: int, to_trainer_id: int) -> int:
        rowcount = self.execute(
            """
            UPDATE PersonalTraining
            SET trainerID = %s
            WHERE trainingID = %s AND trainerID = %s
            """,
            (to_trainer_id, training_id, from_trainer_id),
        )
        self.commit()
        return rowcount

    def add_trainer_busy(self, trainer_id: int, date_from: str, date_to: str, note: str | None = None) -> int:
        self._ensure_trainer_busy_table()
        self.execute(
            """
            INSERT INTO TrainerBusy (trainerID, dateFrom, dateTo, note)
            VALUES (%s, %s, %s, %s)
            """,
            (trainer_id, date_from, date_to, note),
        )
        new_id = self.fetch_scalar("SELECT LAST_INSERT_ID()")
        self.commit()
        return int(new_id) if new_id is not None else 0

    def list_trainer_busy(self, trainer_id: int):
        self._ensure_trainer_busy_table()
        return self.fetch_all(
            """
            SELECT busyID, trainerID, dateFrom, dateTo, note
            FROM TrainerBusy
            WHERE trainerID = %s
            ORDER BY dateFrom DESC, busyID DESC
            """,
            (trainer_id,),
        )

    def list_group_classes_for_trainer(self, trainer_id: int):
        return self.fetch_all(
            """
            SELECT classID, className, classDate, startTime, endTime, hall, maxParticipants, current_participants, classStatus
            FROM GroupClasses
            WHERE trainerID = %s
            ORDER BY classDate, startTime
            """,
            (trainer_id,),
        )

    def list_personal_trainings_for_trainer(self, trainer_id: int):
        return self.fetch_all(
            """
            SELECT trainingID, clientID, goalTraining, trainingDate, startTime, endTime, notes
            FROM PersonalTraining
            WHERE trainerID = %s
            ORDER BY trainingDate, startTime
            """,
            (trainer_id,),
        )

    def get_group_class(self, class_id: int):
        return self.fetch_one(
            """
            SELECT classID, className, trainerID, classDate, startTime, endTime, hall, maxParticipants, current_participants, classStatus
            FROM GroupClasses
            WHERE classID = %s
            """,
            (class_id,),
        )

    def list_group_class_attendance(self, class_id: int):
        return self.fetch_all(
            """
            SELECT ce.enrollmentID,
                   ce.clientID,
                   u.last_name,
                   u.first_name,
                   u.middle_name,
                   ce.status
            FROM ClassEnrollments ce
            JOIN Users u ON u.userID = ce.clientID
            WHERE ce.classID = %s
            ORDER BY u.last_name, u.first_name
            """,
            (class_id,),
        )

    def list_my_clients(self, trainer_id: int):
        return self.fetch_all(
            """
            SELECT DISTINCT u.userID, u.first_name, u.last_name, u.middle_name, u.phone, u.email, u.health_limits, u.birthDate
            FROM Users u
            WHERE u.userType = 'Client'
              AND u.userID IN (
                    SELECT pt.clientID
                    FROM PersonalTraining pt
                    WHERE pt.trainerID = %s
                    UNION
                    SELECT ce.clientID
                    FROM ClassEnrollments ce
                    JOIN GroupClasses gc ON gc.classID = ce.classID
                    WHERE gc.trainerID = %s
              )
            ORDER BY u.last_name, u.first_name
            """,
            (trainer_id, trainer_id),
        )

    def get_client(self, client_id: int):
        return self.fetch_one(
            """
            SELECT userID, first_name, last_name, middle_name, phone, email, health_limits, userType, birthDate
            FROM Users
            WHERE userID = %s AND userType = 'Client'
            """,
            (client_id,),
        )

    def list_client_metrics(self, client_id: int):
        return self.fetch_all(
            """
            SELECT pm.metricID, pm.metricDate, pm.weight, pm.exerciseID, e.name AS exercise_name, pm.notes
            FROM ProgressMetrics pm
            LEFT JOIN exercises e ON e.exerciseID = pm.exerciseID
            WHERE pm.clientID = %s
            ORDER BY pm.metricDate DESC, pm.metricID DESC
            """,
            (client_id,),
        )

    def add_client_metric(self, client_id: int, metric_date: str, notes: str, weight: float | None = None):
        self.execute(
            """
            INSERT INTO ProgressMetrics (clientID, metricDate, weight, exerciseID, notes)
            VALUES (%s, %s, %s, NULL, %s)
            """,
            (client_id, metric_date, weight, notes),
        )
        self.commit()

    def notify_user(self, user_id: int, message: str):
        self.execute(
            """
            INSERT INTO Notifications (userID, message_n)
            VALUES (%s, %s)
            """,
            (user_id, message),
        )
        self.commit()

    def list_directors(self):
        return self.fetch_all(
            """
            SELECT userID
            FROM Users
            WHERE userType = 'Director'
            ORDER BY userID
            """
        )

    def notify_directors(self, message: str):
        directors = self.list_directors()
        if not directors:
            return 0
        params_seq = [(d["userID"], message) for d in directors]
        self.executemany("INSERT INTO Notifications (userID, message_n) VALUES (%s, %s)", params_seq)
        self.commit()
        return len(params_seq)


trainer_dao = TrainerDAO(db)
