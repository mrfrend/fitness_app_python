-- Процедура для получения всех клиентов
DELIMITER //
CREATE PROCEDURE GetAllClients()
BEGIN
    SELECT
        u.userID,
        u.first_name,
        u.last_name,
        u.middle_name,
        u.phone,
        u.email,
        u.birthDate,
        u.health_limits,
        COUNT(DISTINCT m.membID) as active_memberships,
        MAX(m.endDate) as latest_membership_end
    FROM Users u
    LEFT JOIN Memberships m ON u.userID = m.clientID
        AND m.membStatus = 'Active'
    WHERE u.userType = 'Client'
    GROUP BY u.userID
    ORDER BY u.last_name, u.first_name;
END //
DELIMITER ;

-- Процедура для добавления нового клиента
DELIMITER //
CREATE PROCEDURE AddClient(
    IN p_first_name VARCHAR(255),
    IN p_last_name VARCHAR(255),
    IN p_middle_name VARCHAR(255),
    IN p_phone VARCHAR(30),
    IN p_email VARCHAR(100),
    IN p_birthDate DATE,
    IN p_health_limits VARCHAR(550),
    IN p_login VARCHAR(50),
    IN p_password VARCHAR(255)
)
BEGIN
    INSERT INTO Users (
        first_name,
        last_name,
        middle_name,
        phone,
        email,
        birthDate,
        health_limits,
        login,
        password,
        userType
    ) VALUES (
        p_first_name,
        p_last_name,
        p_middle_name,
        p_phone,
        p_email,
        p_birthDate,
        p_health_limits,
        p_login,
        p_password,
        'Client'
    );

    SELECT LAST_INSERT_ID() as new_client_id;
END //
DELIMITER ;

-- Процедура для обновления данных клиента
DELIMITER //
CREATE PROCEDURE UpdateClient(
    IN p_userID INT,
    IN p_first_name VARCHAR(255),
    IN p_last_name VARCHAR(255),
    IN p_middle_name VARCHAR(255),
    IN p_phone VARCHAR(30),
    IN p_email VARCHAR(100),
    IN p_birthDate DATE,
    IN p_health_limits VARCHAR(550)
)
BEGIN
    UPDATE Users
    SET
        first_name = p_first_name,
        last_name = p_last_name,
        middle_name = p_middle_name,
        phone = p_phone,
        email = p_email,
        birthDate = p_birthDate,
        health_limits = p_health_limits
    WHERE userID = p_userID;
END //
DELIMITER ;

-- Процедура для получения активных абонементов клиента
DELIMITER //
CREATE PROCEDURE GetClientMemberships(IN p_clientID INT)
BEGIN
    SELECT
        m.membID,
        m.membType,
        m.startDate,
        m.endDate,
        m.visitsTotal,
        m.visitsUsed,
        m.membStatus,
        m.cost,
        CASE
            WHEN CURDATE() BETWEEN m.startDate AND m.endDate THEN 'Действующий'
            WHEN CURDATE() < m.startDate THEN 'Ожидает начала'
            ELSE 'Истек'
        END as status_text,
        GROUP_CONCAT(z.zoneName SEPARATOR ', ') as zones
    FROM Memberships m
    LEFT JOIN MembershipZones mz ON m.membID = mz.mz_membershipID
    LEFT JOIN Zones z ON mz.mz_zoneID = z.z_zoneID
    WHERE m.clientID = p_clientID
    GROUP BY m.membID
    ORDER BY m.endDate DESC;
END //
DELIMITER ;

-- Процедура для добавления нового абонемента
DELIMITER //
CREATE PROCEDURE AddMembership(
    IN p_clientID INT,
    IN p_membType VARCHAR(100),
    IN p_startDate DATE,
    IN p_endDate DATE,
    IN p_visitsTotal INT,
    IN p_cost DECIMAL(10,2),
    IN p_discountID INT,
    IN p_adminID INT,
    IN p_zone_ids TEXT -- список ID зон через запятую
)
BEGIN
    DECLARE new_memb_id INT;

    -- Вставляем абонемент
    INSERT INTO Memberships (
        clientID, membType, startDate, endDate,
        visitsTotal, visitsUsed, membStatus,
        cost, discountID, adminID
    ) VALUES (
        p_clientID, p_membType, p_startDate, p_endDate,
        p_visitsTotal, 0, 'Active',
        p_cost, p_discountID, p_adminID
    );

    SET new_memb_id = LAST_INSERT_ID();

    -- Добавляем зоны к абонементу
    INSERT INTO MembershipZones (mz_membershipID, mz_zoneID)
    SELECT new_memb_id, CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_zone_ids, ',', numbers.n), ',', -1) AS UNSIGNED)
    FROM (
        SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5
    ) numbers
    WHERE CHAR_LENGTH(p_zone_ids) - CHAR_LENGTH(REPLACE(p_zone_ids, ',', '')) >= numbers.n - 1;

    SELECT new_memb_id as new_membership_id;
END //
DELIMITER ;

-- Процедура для заморозки абонемента
DELIMITER //
CREATE PROCEDURE FreezeMembership(
    IN p_membershipID INT,
    IN p_startDate DATE,
    IN p_endDate DATE
)
BEGIN
    -- Добавляем запись о заморозке
    INSERT INTO MembershipFreezes (mf_membershipID, startDate, endDate)
    VALUES (p_membershipID, p_startDate, p_endDate);

    -- Обновляем статус абонемента
    UPDATE Memberships
    SET membStatus = 'Frozen'
    WHERE membID = p_membershipID;
END //
DELIMITER ;

-- Процедура для разморозки абонемента
DELIMITER //
CREATE PROCEDURE UnfreezeMembership(IN p_membershipID INT)
BEGIN
    -- Обновляем статус абонемента
    UPDATE Memberships
    SET membStatus = 'Active'
    WHERE membID = p_membershipID;
END //
DELIMITER ;

-- Процедура для получения статистики по залам
DELIMITER //
CREATE PROCEDURE GetGymWorkload(
    IN p_date DATE,
    IN p_zone_id INT
)
BEGIN
    SELECT
        z.zoneName,
        DATE_FORMAT(v.visitDate, '%H:00') as hour,
        COUNT(*) as visits_count,
        CONCAT(FLOOR(COUNT(*) * 100 / 20), '%') as occupancy_rate -- 20 макс посещений в час
    FROM Visits v
    JOIN Zones z ON v.v_zoneID = z.z_zoneID
    WHERE v.visitDate = p_date
        AND (p_zone_id IS NULL OR z.z_zoneID = p_zone_id)
    GROUP BY z.zoneName, DATE_FORMAT(v.visitDate, '%H:00')
    ORDER BY z.zoneName, hour;
END //
DELIMITER ;

-- Процедура для получения жалоб и предложений
DELIMITER //
CREATE PROCEDURE GetComplaintsAndSuggestions()
BEGIN
    SELECT
        'Complaint' as type,
        c.complaintID as id,
        CONCAT(u.last_name, ' ', u.first_name) as client_name,
        c.complaintDate as date,
        c.text,
        c.status
    FROM Complaints c
    JOIN Users u ON c.clientID = u.userID

    UNION ALL

    SELECT
        'Suggestion' as type,
        r.reviewID as id,
        CONCAT(u.last_name, ' ', u.first_name) as client_name,
        DATE(r.dataRev) as date,
        r.textRev as text,
        'Closed' as status
    FROM Review r
    JOIN Users u ON r.clientID = u.userID
    WHERE r.reviewType = 'Suggestion'

    ORDER BY date DESC;
END //
DELIMITER ;