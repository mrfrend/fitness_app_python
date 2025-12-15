from app.core.dao import BaseDAO
from app.database import db


class ClientDAO(BaseDAO):
    def __init__(self):
        super().__init__(db)

    # ========== АВТОРИЗАЦИЯ ==========

    def authenticate_user(self, login: str, password: str, user_type: str) -> dict:
        """Аутентификация пользователя"""
        with self.db.conn.cursor() as cursor:
            query = """
                SELECT userID, first_name, last_name, middle_name, phone, email,
                       health_limits, birthDate, userType
                FROM Users 
                WHERE login = %s AND password = %s AND userType = %s
            """
            cursor.execute(query, (login, password, user_type))
            user = cursor.fetchone()
            self.db.conn.commit()
            return user

    # ========== ИНФОРМАЦИЯ О КЛИЕНТЕ ==========

    # ========== ИНФОРМАЦИЯ О КЛИЕНТЕ ==========

    def get_client_info(self, client_id: int) -> dict:
        """Получение информации о клиенте"""
        with self.db.conn.cursor() as cursor:
            query = """
                SELECT 
                    userID,
                    first_name,
                    last_name,
                    middle_name,
                    CONCAT(last_name, ' ', first_name, ' ', 
                           COALESCE(middle_name, '')) as full_name,
                    phone,
                    email,
                    health_limits,
                    birthDate,
                    userType
                FROM Users 
                WHERE userID = %s
            """
            cursor.execute(query, (client_id,))
            result = cursor.fetchone()
            self.db.conn.commit()
            return result

    def update_client_info(self, client_id: int, **data):
        """Обновление информации о клиенте"""
        with self.db.conn.cursor() as cursor:
            query = """
                UPDATE Users 
                SET height = %s, goal = %s, email = %s, phone = %s, 
                    health_limits = %s, birthDate = %s
                WHERE userID = %s
            """
            cursor.execute(query, (
                data.get('height'), data.get('goal'), data.get('email'),
                data.get('phone'), data.get('health_limits'), data.get('birthDate'),
                client_id
            ))
            self.db.conn.commit()

    # ========== ЗАНЯТИЯ (ОБЩИЕ МЕТОДЫ) ==========

    def get_available_classes(self, client_id: int) -> list:
        """Получение всех доступных занятий (групповых и индивидуальных)"""
        available_classes = []

        # Групповые занятия
        with self.db.conn.cursor() as cursor:
            query = """
                SELECT 
                    gc.classID as id,
                    gc.className as name,
                    CONCAT(u.last_name, ' ', LEFT(u.first_name, 1), '. ', 
                           LEFT(u.middle_name, 1), '.') as trainer_name,
                    gc.classDate as date,
                    gc.startTime as start_time,
                    gc.endTime as end_time,
                    gc.hall,
                    gc.maxParticipants as max_participants,
                    gc.current_participants as current_participants,
                    'group' as class_type,
                    gc.classStatus as status,
                    CASE 
                        WHEN ce.enrollmentID IS NOT NULL THEN 'enrolled'
                        WHEN gc.current_participants >= gc.maxParticipants THEN 'full'
                        WHEN gc.classDate < CURDATE() OR 
                            (gc.classDate = CURDATE() AND gc.startTime < CURTIME()) THEN 'past'
                        ELSE 'available'
                    END as availability
                FROM GroupClasses gc
                JOIN Users u ON gc.trainerID = u.userID
                LEFT JOIN ClassEnrollments ce ON gc.classID = ce.classID 
                    AND ce.clientID = %s AND ce.status = 'Enrolled'
                WHERE gc.classStatus = 'Scheduled'
                ORDER BY gc.classDate, gc.startTime
            """
            cursor.execute(query, (client_id,))
            group_classes = cursor.fetchall()
            available_classes.extend(group_classes)

        # Индивидуальные занятия (где clientID IS NULL)
        with self.db.conn.cursor() as cursor:
            query = """
                SELECT 
                    pt.trainingID as id,
                    CONCAT('Индивидуальная тренировка (', 
                           CONCAT(u.last_name, ' ', LEFT(u.first_name, 1), '. ', 
                                  LEFT(u.middle_name, 1), '.'), ')') as name,
                    CONCAT(u.last_name, ' ', LEFT(u.first_name, 1), '. ', 
                           LEFT(u.middle_name, 1), '.') as trainer_name,
                    pt.trainingDate as date,
                    pt.startTime as start_time,
                    pt.endTime as end_time,
                    'Зал для индивидуальных тренировок' as hall,
                    1 as max_participants,
                    CASE WHEN pt.clientID IS NOT NULL THEN 1 ELSE 0 END as current_participants,
                    'individual' as class_type,
                    'Scheduled' as status,
                    CASE 
                        WHEN pt.clientID IS NOT NULL THEN 'occupied'
                        WHEN pt.clientID = %s THEN 'enrolled'
                        WHEN pt.trainingDate < CURDATE() OR 
                            (pt.trainingDate = CURDATE() AND pt.startTime < CURTIME()) THEN 'past'
                        ELSE 'available'
                    END as availability
                FROM PersonalTraining pt
                JOIN Users u ON pt.trainerID = u.userID
                WHERE pt.clientID IS NULL OR pt.clientID = %s
                ORDER BY pt.trainingDate, pt.startTime
            """
            cursor.execute(query, (client_id, client_id))
            individual_classes = cursor.fetchall()
            available_classes.extend(individual_classes)

        self.db.conn.commit()
        return available_classes

    def get_filtered_classes(self, client_id: int, class_type: str = None) -> list:
        """Получение занятий с фильтрацией по типу"""
        all_classes = self.get_available_classes(client_id)

        if not class_type or class_type == 'Все':
            return all_classes

        if class_type == 'Групповые':
            return [c for c in all_classes if c['class_type'] == 'group']
        else:  # 'Индивидуальные'
            return [c for c in all_classes if c['class_type'] == 'individual']

    # ========== ЗАПИСЬ НА ЗАНЯТИЯ ==========

    def enroll_to_class(self, client_id: int, class_id: int, class_type: str) -> bool:
        """Запись клиента на занятие"""
        try:
            with self.db.conn.cursor() as cursor:
                if class_type == 'group':
                    # Проверяем, не записан ли уже
                    check_query = """
                        SELECT enrollmentID FROM ClassEnrollments 
                        WHERE clientID = %s AND classID = %s AND status = 'Enrolled'
                    """
                    cursor.execute(check_query, (client_id, class_id))
                    if cursor.fetchone():
                        return False  # Уже записан

                    # Проверяем, есть ли свободные места
                    check_capacity = """
                        SELECT current_participants, maxParticipants 
                        FROM GroupClasses 
                        WHERE classID = %s
                    """
                    cursor.execute(check_capacity, (class_id,))
                    class_info = cursor.fetchone()

                    if class_info['current_participants'] >= class_info['maxParticipants']:
                        return False  # Мест нет

                    # Записываем
                    enroll_query = """
                        INSERT INTO ClassEnrollments (classID, clientID, status)
                        VALUES (%s, %s, 'Enrolled')
                    """
                    cursor.execute(enroll_query, (class_id, client_id))

                    # Увеличиваем счетчик участников
                    update_query = """
                        UPDATE GroupClasses 
                        SET current_participants = current_participants + 1
                        WHERE classID = %s
                    """
                    cursor.execute(update_query, (class_id,))

                else:  # individual
                    # Проверяем, не занято ли уже
                    check_query = """
                        SELECT clientID FROM PersonalTraining 
                        WHERE trainingID = %s
                    """
                    cursor.execute(check_query, (class_id,))
                    training = cursor.fetchone()

                    if training['clientID'] is not None:
                        return False  # Уже занято

                    # Записываем клиента
                    update_query = """
                        UPDATE PersonalTraining 
                        SET clientID = %s
                        WHERE trainingID = %s
                    """
                    cursor.execute(update_query, (client_id, class_id))

                self.db.conn.commit()
                return True

        except Exception as e:
            self.db.conn.rollback()
            print(f"Ошибка при записи на занятие: {e}")
            return False

    # ========== МОИ ЗАПИСИ ==========

    def get_client_enrollments(self, client_id: int) -> list:
        """Получение активных записей клиента"""
        enrollments = []

        # Групповые занятия
        with self.db.conn.cursor() as cursor:
            query = """
                SELECT 
                    ce.enrollmentID as id,
                    gc.classID as class_id,
                    gc.className as name,
                    CONCAT(u.last_name, ' ', LEFT(u.first_name, 1), '. ', 
                           LEFT(u.middle_name, 1), '.') as trainer_name,
                    gc.classDate as date,
                    gc.startTime as time,
                    'group' as class_type,
                    ce.status,
                    CASE 
                        WHEN gc.classDate < CURDATE() OR 
                            (gc.classDate = CURDATE() AND gc.startTime < CURTIME()) THEN 'past'
                        ELSE 'future'
                    END as time_status
                FROM ClassEnrollments ce
                JOIN GroupClasses gc ON ce.classID = gc.classID
                JOIN Users u ON gc.trainerID = u.userID
                WHERE ce.clientID = %s AND ce.status = 'Enrolled'
                ORDER BY gc.classDate, gc.startTime
            """
            cursor.execute(query, (client_id,))
            group_enrollments = cursor.fetchall()
            enrollments.extend(group_enrollments)

        # Индивидуальные занятия
        with self.db.conn.cursor() as cursor:
            query = """
                SELECT 
                    pt.trainingID as id,
                    pt.trainingID as class_id,
                    CONCAT('Индивидуальная тренировка') as name,
                    CONCAT(u.last_name, ' ', LEFT(u.first_name, 1), '. ', 
                           LEFT(u.middle_name, 1), '.') as trainer_name,
                    pt.trainingDate as date,
                    pt.startTime as time,
                    'individual' as class_type,
                    'Enrolled' as status,
                    CASE 
                        WHEN pt.trainingDate < CURDATE() OR 
                            (pt.trainingDate = CURDATE() AND pt.startTime < CURTIME()) THEN 'past'
                        ELSE 'future'
                    END as time_status
                FROM PersonalTraining pt
                JOIN Users u ON pt.trainerID = u.userID
                WHERE pt.clientID = %s
                ORDER BY pt.trainingDate, pt.startTime
            """
            cursor.execute(query, (client_id,))
            individual_enrollments = cursor.fetchall()
            enrollments.extend(individual_enrollments)

        self.db.conn.commit()
        return enrollments

    def cancel_enrollment(self, enrollment_id: int, client_id: int, class_type: str) -> bool:
        """Отмена записи клиента"""
        try:
            with self.db.conn.cursor() as cursor:
                if class_type == 'group':
                    # Получаем classID для уменьшения счетчика
                    get_class_query = """
                        SELECT ce.classID 
                        FROM ClassEnrollments ce
                        WHERE ce.enrollmentID = %s AND ce.clientID = %s
                    """
                    cursor.execute(get_class_query, (enrollment_id, client_id))
                    result = cursor.fetchone()

                    if not result:
                        return False

                    class_id = result['classID']

                    # Обновляем статус записи
                    cancel_query = """
                        UPDATE ClassEnrollments 
                        SET status = 'Canceled'
                        WHERE enrollmentID = %s AND clientID = %s
                    """
                    cursor.execute(cancel_query, (enrollment_id, client_id))

                    # Уменьшаем счетчик участников
                    update_query = """
                        UPDATE GroupClasses 
                        SET current_participants = GREATEST(0, current_participants - 1)
                        WHERE classID = %s
                    """
                    cursor.execute(update_query, (class_id,))

                else:  # individual
                    # Освобождаем занятие (устанавливаем clientID в NULL)
                    cancel_query = """
                        UPDATE PersonalTraining 
                        SET clientID = NULL
                        WHERE trainingID = %s AND clientID = %s
                    """
                    cursor.execute(cancel_query, (enrollment_id, client_id))

                self.db.conn.commit()
                return True

        except Exception as e:
            self.db.conn.rollback()
            print(f"Ошибка при отмене записи: {e}")
            return False

    # ========== ИСТОРИЯ ПОСЕЩЕНИЙ ==========

    def get_client_history(self, client_id: int) -> list:
        """Получение истории посещений клиента"""
        history = []

        # Групповые занятия (посещенные)
        with self.db.conn.cursor() as cursor:
            query = """
                SELECT 
                    ce.enrollmentID as id,
                    gc.className as name,
                    gc.classDate as date,
                    gc.startTime as time,
                    'group' as class_type,
                    ce.status
                FROM ClassEnrollments ce
                JOIN GroupClasses gc ON ce.classID = gc.classID
                WHERE ce.clientID = %s 
                    AND ce.status IN ('Attended', 'Absent')
                    AND (gc.classDate < CURDATE() OR 
                        (gc.classDate = CURDATE() AND gc.endTime < CURTIME()))
                ORDER BY gc.classDate DESC, gc.startTime DESC
            """
            cursor.execute(query, (client_id,))
            group_history = cursor.fetchall()
            history.extend(group_history)

        # Индивидуальные занятия (прошедшие)
        with self.db.conn.cursor() as cursor:
            query = """
                SELECT 
                    pt.trainingID as id,
                    CONCAT('Индивидуальная тренировка') as name,
                    pt.trainingDate as date,
                    pt.startTime as time,
                    'individual' as class_type,
                    'Attended' as status
                FROM PersonalTraining pt
                WHERE pt.clientID = %s
                    AND (pt.trainingDate < CURDATE() OR 
                        (pt.trainingDate = CURDATE() AND pt.endTime < CURTIME()))
                ORDER BY pt.trainingDate DESC, pt.startTime DESC
            """
            cursor.execute(query, (client_id,))
            individual_history = cursor.fetchall()
            history.extend(individual_history)

        self.db.conn.commit()
        return history

    # ========== ОТЗЫВЫ ==========

    # ========== ОТЗЫВЫ И ЖАЛОБЫ ==========

    def save_review(self, client_id: int, review_type: str, text: str, review_date: str) -> bool:
        """Сохранение пожелания в таблицу Review"""
        try:
            with self.db.conn.cursor() as cursor:
                query = """
                    INSERT INTO Review (clientID, reviewType, dataRev, textRev)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (client_id, review_type, review_date, text))
                self.db.conn.commit()
                return True

        except Exception as e:
            self.db.conn.rollback()
            print(f"Ошибка при сохранении отзыва: {e}")
            return False

    def save_complaint(self, client_id: int, text: str, complaint_date: str) -> bool:
        """Сохранение жалобы в таблицу Complaints"""
        try:
            with self.db.conn.cursor() as cursor:
                query = """
                    INSERT INTO Complaints (clientID, complaintDate, text, status)
                    VALUES (%s, %s, %s, 'New')
                """
                cursor.execute(query, (client_id, complaint_date, text))
                self.db.conn.commit()
                return True

        except Exception as e:
            self.db.conn.rollback()
            print(f"Ошибка при сохранении жалобы: {e}")
            return False

    # ========== ПРОГРЕСС ==========

    # ========== ПРОГРЕСС ==========

    def get_progress_metrics(self, client_id: int) -> list:
        """Получение метрик прогресса клиента (без роста)"""
        with self.db.conn.cursor() as cursor:
            query = """
                SELECT 
                    metricDate as measurement_date,
                    weight,
                    notes as result
                FROM ProgressMetrics
                WHERE clientID = %s
                ORDER BY metricDate DESC
            """
            cursor.execute(query, (client_id,))
            metrics = cursor.fetchall()
            self.db.conn.commit()
            return metrics

    # ========== ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ ==========

    def check_class_availability(self, class_id: int, class_type: str) -> dict:
        """Проверка доступности занятия"""
        with self.db.conn.cursor() as cursor:
            if class_type == 'group':
                query = """
                    SELECT 
                        current_participants,
                        maxParticipants,
                        classDate,
                        startTime,
                        className
                    FROM GroupClasses
                    WHERE classID = %s
                """
            else:  # individual
                query = """
                    SELECT 
                        clientID,
                        trainingDate as classDate,
                        startTime,
                        goalTraining as className
                    FROM PersonalTraining
                    WHERE trainingID = %s
                """

            cursor.execute(query, (class_id,))
            result = cursor.fetchone()
            self.db.conn.commit()
            return result

    # ========== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ==========

    def format_date_for_display(self, date_obj):
        """Форматирование даты для отображения"""
        if not date_obj:
            return ""
        if isinstance(date_obj, str):
            return date_obj
        return date_obj.strftime('%d.%m.%Y')

    def format_time_for_display(self, time_obj):
        """Форматирование времени для отображения"""
        if not time_obj:
            return ""
        if isinstance(time_obj, str):
            return time_obj
        return time_obj.strftime('%H:%M')

    def get_current_datetime(self):
        """Получение текущей даты и времени"""
        from datetime import datetime
        return datetime.now()