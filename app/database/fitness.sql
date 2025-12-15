-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 15, 2025 at 11:03 PM
-- Server version: 8.0.30
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fitness`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`%` PROCEDURE `AddClient` (IN `p_first_name` VARCHAR(255), IN `p_last_name` VARCHAR(255), IN `p_middle_name` VARCHAR(255), IN `p_phone` VARCHAR(30), IN `p_email` VARCHAR(100), IN `p_birthDate` DATE, IN `p_health_limits` VARCHAR(550), IN `p_login` VARCHAR(50), IN `p_password` VARCHAR(255))   BEGIN
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
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `AddMembership` (IN `p_clientID` INT, IN `p_membType` VARCHAR(100), IN `p_startDate` DATE, IN `p_endDate` DATE, IN `p_visitsTotal` INT, IN `p_cost` DECIMAL(10,2), IN `p_discountID` INT, IN `p_adminID` INT, IN `p_zone_ids` TEXT)   BEGIN
    DECLARE new_memb_id INT;

    
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

    
    INSERT INTO MembershipZones (mz_membershipID, mz_zoneID)
    SELECT new_memb_id, CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_zone_ids, ',', numbers.n), ',', -1) AS UNSIGNED)
    FROM (
        SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5
    ) numbers
    WHERE CHAR_LENGTH(p_zone_ids) - CHAR_LENGTH(REPLACE(p_zone_ids, ',', '')) >= numbers.n - 1;

    SELECT new_memb_id as new_membership_id;
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `FreezeMembership` (IN `p_membershipID` INT, IN `p_startDate` DATE, IN `p_endDate` DATE)   BEGIN
    
    INSERT INTO MembershipFreezes (mf_membershipID, startDate, endDate)
    VALUES (p_membershipID, p_startDate, p_endDate);

    
    UPDATE Memberships
    SET membStatus = 'Frozen'
    WHERE membID = p_membershipID;
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `GetAllClients` ()   BEGIN
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
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `GetClientMemberships` (IN `p_clientID` INT)   BEGIN
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
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `GetComplaintsAndSuggestions` ()   BEGIN
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
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `GetGymWorkload` (IN `p_date` DATE, IN `p_zone_id` INT)   BEGIN
    SELECT
        z.zoneName,
        DATE_FORMAT(v.visitDate, '%H:00') as hour,
        COUNT(*) as visits_count,
        CONCAT(FLOOR(COUNT(*) * 100 / 20), '%') as occupancy_rate 
    FROM Visits v
    JOIN Zones z ON v.v_zoneID = z.z_zoneID
    WHERE v.visitDate = p_date
        AND (p_zone_id IS NULL OR z.z_zoneID = p_zone_id)
    GROUP BY z.zoneName, DATE_FORMAT(v.visitDate, '%H:00')
    ORDER BY z.zoneName, hour;
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `UnfreezeMembership` (IN `p_membershipID` INT)   BEGIN
    
    UPDATE Memberships
    SET membStatus = 'Active'
    WHERE membID = p_membershipID;
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `UpdateClient` (IN `p_userID` INT, IN `p_first_name` VARCHAR(255), IN `p_last_name` VARCHAR(255), IN `p_middle_name` VARCHAR(255), IN `p_phone` VARCHAR(30), IN `p_email` VARCHAR(100), IN `p_birthDate` DATE, IN `p_health_limits` VARCHAR(550))   BEGIN
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
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `ClassEnrollments`
--

CREATE TABLE `ClassEnrollments` (
  `enrollmentID` int NOT NULL,
  `classID` int NOT NULL,
  `clientID` int NOT NULL,
  `status` enum('Enrolled','Canceled','Attended','Absent') DEFAULT 'Enrolled'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `ClassEnrollments`
--

INSERT INTO `ClassEnrollments` (`enrollmentID`, `classID`, `clientID`, `status`) VALUES
(1, 1, 16, 'Attended'),
(2, 1, 26, 'Enrolled'),
(3, 2, 21, 'Attended'),
(4, 2, 30, 'Canceled'),
(5, 3, 34, 'Enrolled'),
(6, 3, 16, 'Absent'),
(7, 4, 21, 'Enrolled'),
(8, 4, 26, 'Attended'),
(9, 5, 30, 'Enrolled'),
(10, 5, 34, 'Enrolled'),
(11, 9, 16, 'Canceled'),
(12, 9, 16, 'Enrolled');

-- --------------------------------------------------------

--
-- Table structure for table `Complaints`
--

CREATE TABLE `Complaints` (
  `complaintID` int NOT NULL,
  `clientID` int NOT NULL,
  `complaintDate` date NOT NULL,
  `text` varchar(250) NOT NULL,
  `status` enum('New','InProgress','Closed') DEFAULT 'New'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Complaints`
--

INSERT INTO `Complaints` (`complaintID`, `clientID`, `complaintDate`, `text`, `status`) VALUES
(1, 16, '2024-06-15', 'Слишком холодно в зале 2 во время занятий.', 'InProgress'),
(2, 30, '2024-06-15', 'Не работал один из кардиотренажеров.', 'New'),
(3, 34, '2024-06-16', 'Хотелось бы больше вечерних занятий по йоге.', 'Closed');

-- --------------------------------------------------------

--
-- Table structure for table `discount`
--

CREATE TABLE `discount` (
  `discountID` int NOT NULL,
  `percentage_disc` decimal(5,2) NOT NULL,
  `dateStart` date NOT NULL,
  `dateEnd` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `discount`
--

INSERT INTO `discount` (`discountID`, `percentage_disc`, `dateStart`, `dateEnd`) VALUES
(1, '10.00', '2024-06-01', '2024-06-30'),
(2, '15.00', '2024-01-01', '2024-12-31'),
(3, '5.00', '2024-06-15', '2024-06-30');

-- --------------------------------------------------------

--
-- Table structure for table `Equipment`
--

CREATE TABLE `Equipment` (
  `equipmentID` int NOT NULL,
  `name_e` varchar(100) NOT NULL,
  `quantityExist` int NOT NULL,
  `quantityLeft` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Equipment`
--

INSERT INTO `Equipment` (`equipmentID`, `name_e`, `quantityExist`, `quantityLeft`) VALUES
(2, 'Штанги', 12, 2),
(5, 'Пояса тяжелоатлетические', 10, 1);

-- --------------------------------------------------------

--
-- Table structure for table `exercises`
--

CREATE TABLE `exercises` (
  `exerciseID` int NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `exercises`
--

INSERT INTO `exercises` (`exerciseID`, `name`) VALUES
(1, 'Жим лежа'),
(2, 'Приседания'),
(3, 'Тяга блока'),
(4, 'Асаны йоги'),
(5, 'Растяжка'),
(6, 'Становая тяга'),
(7, 'Жим гантелей'),
(8, 'Планка'),
(9, 'Бёрпи');

-- --------------------------------------------------------

--
-- Table structure for table `GroupClasses`
--

CREATE TABLE `GroupClasses` (
  `classID` int NOT NULL,
  `className` varchar(255) NOT NULL,
  `trainerID` int NOT NULL,
  `classDate` date NOT NULL,
  `startTime` time NOT NULL,
  `endTime` time NOT NULL,
  `hall` varchar(100) DEFAULT NULL,
  `maxParticipants` int DEFAULT NULL,
  `current_participants` int NOT NULL,
  `classStatus` enum('Scheduled','Full','Canceled') DEFAULT 'Scheduled'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `GroupClasses`
--

INSERT INTO `GroupClasses` (`classID`, `className`, `trainerID`, `classDate`, `startTime`, `endTime`, `hall`, `maxParticipants`, `current_participants`, `classStatus`) VALUES
(1, 'Йога для начинающих', 9, '2024-06-16', '10:00:00', '11:00:00', 'Зал 2', 15, 12, 'Scheduled'),
(2, 'Силовая аэробика', 7, '2024-06-16', '18:00:00', '19:00:00', 'Зал 1', 20, 18, 'Scheduled'),
(3, 'Пилатес', 9, '2024-06-17', '11:00:00', '12:00:00', 'Зал 2', 12, 12, 'Full'),
(4, 'Аквааэробика', 11, '2024-06-17', '15:00:00', '16:00:00', 'Бассейн', 10, 7, 'Scheduled'),
(5, 'Бокс', 7, '2024-06-18', '19:00:00', '20:30:00', 'Зал 3', 8, 5, 'Scheduled'),
(6, 'Силовая аэробика', 9, '2024-06-22', '09:00:00', '10:00:00', NULL, 20, 0, 'Scheduled'),
(7, 'Силовая аэробика', 7, '2024-06-16', '09:00:00', '10:00:00', NULL, 20, 0, 'Scheduled'),
(8, 'Баскетбол', 7, '2025-12-15', '09:00:00', '10:00:00', NULL, 20, 0, 'Scheduled'),
(9, 'Футбольчик', 7, '2025-12-17', '09:00:00', '09:35:00', 'Зал для групповых тренировок', 30, 11, 'Scheduled');

-- --------------------------------------------------------

--
-- Table structure for table `MembershipFreezes`
--

CREATE TABLE `MembershipFreezes` (
  `freezeID` int NOT NULL,
  `mf_membershipID` int NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Memberships`
--

CREATE TABLE `Memberships` (
  `membID` int NOT NULL,
  `clientID` int NOT NULL,
  `membType` varchar(100) NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `visitsTotal` int DEFAULT NULL,
  `visitsUsed` int DEFAULT '0',
  `membStatus` enum('Active','Frozen','Completed') DEFAULT 'Active',
  `cost` decimal(10,2) DEFAULT NULL,
  `discountID` int DEFAULT NULL,
  `adminID` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Memberships`
--

INSERT INTO `Memberships` (`membID`, `clientID`, `membType`, `startDate`, `endDate`, `visitsTotal`, `visitsUsed`, `membStatus`, `cost`, `discountID`, `adminID`) VALUES
(1, 16, 'Месячный безлимит', '2024-06-01', '2024-06-30', 999, 42, 'Active', '5000.00', NULL, 2),
(2, 21, '12 посещений', '2024-06-05', '2024-09-05', 12, 8, 'Active', '3000.00', NULL, 2),
(3, 26, 'Годовой VIP', '2024-01-10', '2025-01-10', 999, 156, 'Active', '60000.00', NULL, 4),
(4, 30, 'Разовое посещение', '2024-06-15', '2024-06-15', 1, 1, 'Completed', '10000.00', NULL, 2),
(5, 34, 'Квартальный', '2024-06-01', '2024-08-31', 999, 15, 'Active', '10800.00', 1, 4);

-- --------------------------------------------------------

--
-- Table structure for table `MembershipZones`
--

CREATE TABLE `MembershipZones` (
  `memberzoneID` int NOT NULL,
  `mz_membershipID` int NOT NULL,
  `mz_zoneID` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `MembershipZones`
--

INSERT INTO `MembershipZones` (`memberzoneID`, `mz_membershipID`, `mz_zoneID`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 2, 1),
(5, 3, 1),
(6, 3, 2),
(7, 3, 3),
(8, 4, 1),
(9, 5, 1),
(10, 5, 3);

-- --------------------------------------------------------

--
-- Table structure for table `Notifications`
--

CREATE TABLE `Notifications` (
  `notificationID` int NOT NULL,
  `userID` int NOT NULL,
  `message_n` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sentDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `status_n` enum('Unread','Read') DEFAULT 'Unread'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Notifications`
--

INSERT INTO `Notifications` (`notificationID`, `userID`, `message_n`, `sentDate`, `status_n`) VALUES
(1, 16, 'Напоминание: у вас занятие \"Йога для начинающих\" 2024-06-16 в 10:00.', '2024-06-16 08:00:00', 'Unread'),
(2, 21, 'Напоминание: персональная тренировка 2024-06-12 в 14:00.', '2024-06-12 11:00:00', 'Read'),
(3, 34, 'Вы записаны на занятие \"Бокс\" 2024-06-18 в 19:00.', '2024-06-17 12:00:00', 'Unread'),
(4, 16, 'Современные технологии достигли такого уровня, что курс на социально-ориентированный национальный проект требует анализа поставленных обществом задач. Не следует, однако, забывать, что перспективное планирование требует от нас анализа поэтапного и последовательного развития общества.', '2025-12-15 20:12:15', 'Unread'),
(5, 21, 'Современные технологии достигли такого уровня, что курс на социально-ориентированный национальный проект требует анализа поставленных обществом задач. Не следует, однако, забывать, что перспективное планирование требует от нас анализа поэтапного и последовательного развития общества.', '2025-12-15 20:12:15', 'Unread'),
(6, 26, 'Современные технологии достигли такого уровня, что курс на социально-ориентированный национальный проект требует анализа поставленных обществом задач. Не следует, однако, забывать, что перспективное планирование требует от нас анализа поэтапного и последовательного развития общества.', '2025-12-15 20:12:15', 'Unread'),
(7, 30, 'Современные технологии достигли такого уровня, что курс на социально-ориентированный национальный проект требует анализа поставленных обществом задач. Не следует, однако, забывать, что перспективное планирование требует от нас анализа поэтапного и последовательного развития общества.', '2025-12-15 20:12:15', 'Unread'),
(8, 34, 'Современные технологии достигли такого уровня, что курс на социально-ориентированный национальный проект требует анализа поставленных обществом задач. Не следует, однако, забывать, что перспективное планирование требует от нас анализа поэтапного и последовательного развития общества.', '2025-12-15 20:12:15', 'Unread'),
(9, 21, 'Aboba', '2025-12-15 20:12:28', 'Unread');

-- --------------------------------------------------------

--
-- Table structure for table `PersExercises`
--

CREATE TABLE `PersExercises` (
  `PersExerciseID` int NOT NULL,
  `exerciseID` int DEFAULT NULL,
  `personaltrainingID` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `PersExercises`
--

INSERT INTO `PersExercises` (`PersExerciseID`, `exerciseID`, `personaltrainingID`) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 1),
(4, 4, 2),
(5, 5, 2),
(6, 6, 3),
(7, 7, 3);

-- --------------------------------------------------------

--
-- Table structure for table `PersonalTraining`
--

CREATE TABLE `PersonalTraining` (
  `trainingID` int NOT NULL,
  `clientID` int NOT NULL,
  `trainerID` int NOT NULL,
  `goalTraining` varchar(250) NOT NULL,
  `trainingDate` date NOT NULL,
  `startTime` time NOT NULL,
  `endTime` time NOT NULL,
  `notes` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `PersonalTraining`
--

INSERT INTO `PersonalTraining` (`trainingID`, `clientID`, `trainerID`, `goalTraining`, `trainingDate`, `startTime`, `endTime`, `notes`) VALUES
(1, 26, 7, 'Набор мышечной массы', '2024-06-14', '16:00:00', '17:00:00', 'Хорошая техника'),
(2, 16, 9, 'Гибкость и осанка', '2024-06-13', '10:00:00', '11:00:00', 'Улучшилась гибкость'),
(3, 21, 7, 'Силовая подготовка', '2024-06-12', '14:00:00', '15:00:00', 'Нужно работать над техникой');

-- --------------------------------------------------------

--
-- Table structure for table `ProgressMetrics`
--

CREATE TABLE `ProgressMetrics` (
  `metricID` int NOT NULL,
  `clientID` int NOT NULL,
  `metricDate` date NOT NULL,
  `weight` decimal(5,2) DEFAULT NULL,
  `exerciseID` int DEFAULT NULL,
  `notes` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `ProgressMetrics`
--

INSERT INTO `ProgressMetrics` (`metricID`, `clientID`, `metricDate`, `weight`, `exerciseID`, `notes`) VALUES
(1, 26, '2024-06-14', '72.50', 1, 'Жим 80кг x 8'),
(2, 21, '2024-06-12', '83.00', 6, 'Становая 60кг x 6'),
(3, 16, '2024-06-13', '60.00', 5, 'Растяжка: 15 минут'),
(4, 34, '2024-06-15', '55.50', NULL, 'Общее самочувствие хорошее');

-- --------------------------------------------------------

--
-- Table structure for table `Review`
--

CREATE TABLE `Review` (
  `reviewID` int NOT NULL,
  `reviewType` enum('Complaint','Suggestion') DEFAULT NULL,
  `dataRev` datetime DEFAULT CURRENT_TIMESTAMP,
  `textRev` text NOT NULL,
  `clientID` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Review`
--

INSERT INTO `Review` (`reviewID`, `reviewType`, `dataRev`, `textRev`, `clientID`) VALUES
(1, 'Suggestion', '2024-06-16 09:30:00', 'Добавьте, пожалуйста, возможность видеть свободные места в группах.', 21),
(2, 'Complaint', '2024-06-15 20:45:00', 'Очередь на ресепшене в вечернее время.', 34),
(3, 'Suggestion', '2025-12-15 21:33:18', 'Очень хорошо!', 16);

-- --------------------------------------------------------

--
-- Table structure for table `TrainerSpecializations`
--

CREATE TABLE `TrainerSpecializations` (
  `trainer_specialization_id` int NOT NULL,
  `trainerID` int NOT NULL,
  `specialization` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `userID` int NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `middle_name` varchar(255) DEFAULT NULL,
  `phone` varchar(30) NOT NULL,
  `email` varchar(100) NOT NULL,
  `health_limits` varchar(550) NOT NULL,
  `login` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `userType` enum('Director','Administrator','Trainer','Client') NOT NULL,
  `birthDate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`userID`, `first_name`, `last_name`, `middle_name`, `phone`, `email`, `health_limits`, `login`, `password`, `userType`, `birthDate`) VALUES
(1, 'Марина', 'Сидорова', 'Петровна', '89219014567', 'director@fitness.ru', 'Нет', 'director1', 'pass1', 'Director', '1980-05-15'),
(2, 'Анна', 'Романова', 'Сергеевна', '89210125678', 'admin1@fitness.ru', 'Нет', 'admin1', 'pass2', 'Administrator', '1992-08-22'),
(4, 'Елена', 'Яковлева', 'Викторовна', '89211236789', 'admin2@fitness.ru', 'Нет', 'admin2', 'pass3', 'Trainer', '1988-11-10'),
(7, 'Дмитрий', 'Петров', 'Александрович', '89212347890', 'petrov@fitness.ru', 'Ограничение: травма плеча (небольшие веса)', 'trainer1', 'pass4', 'Trainer', '1985-03-18'),
(9, 'Ольга', 'Смирнова', 'Игоревна', '89213458901', 'smirnova@fitness.ru', 'Нет', 'trainer2', 'pass5', 'Trainer', '1990-07-25'),
(11, 'Сергей', 'Козлов', 'Николаевич', '89214569012', 'kozlov@fitness.ru', 'Нет', 'trainer3', 'pass6', 'Administrator', '1987-12-05'),
(16, 'Екатерина', 'Федорова', 'Дмитриевна', '89161112236', 'fedorova@mail.ru', 'Ограничение: колено (без прыжков)', 'client1', 'pass7', 'Client', '1995-04-12'),
(21, 'Алексей', 'Михайлов', 'Владимирович', '89162223347', 'mikhailov@gmail.com', 'Нет', 'client2', 'pass8', 'Client', '1988-09-30'),
(26, 'Ирина', 'Иванова', 'Сергеевна', '89163334459', 'novikova@yandex.ru', 'Нет', 'client3', 'pass9', 'Client', '1992-06-18'),
(30, 'Игорь', 'Соколов', 'Петрович', '89164445569', 'sokolov@mail.ru', 'Ограничение: давление (умеренная нагрузка)', 'client4', 'pass10', 'Client', '1983-02-28'),
(34, 'Мария', 'Павлова', 'Александровна', '89165556670', 'pavlova@gmail.com', 'Нет', 'client5', 'pass11', 'Client', '1997-11-07'),
(36, 'фывыфв', 'ыщьу', 'фывфывфы', '1312312', 'desadas', 'Нет', '1312312', '1312312', 'Client', '2007-12-15');

-- --------------------------------------------------------

--
-- Table structure for table `Visits`
--

CREATE TABLE `Visits` (
  `visitID` int NOT NULL,
  `clientID` int NOT NULL,
  `visitDate` date NOT NULL,
  `checkInTime` time DEFAULT NULL,
  `checkOutTime` time DEFAULT NULL,
  `v_zoneID` int DEFAULT NULL,
  `v_membershipID` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Visits`
--

INSERT INTO `Visits` (`visitID`, `clientID`, `visitDate`, `checkInTime`, `checkOutTime`, `v_zoneID`, `v_membershipID`) VALUES
(1, 16, '2024-06-15', '08:30:00', '10:15:00', 1, 1),
(2, 21, '2024-06-15', '09:00:00', '10:30:00', 1, 2),
(3, 26, '2024-06-15', '07:00:00', '08:30:00', 2, 3),
(4, 16, '2024-06-15', '18:00:00', '19:45:00', 3, 1),
(5, 34, '2024-06-15', '19:00:00', '20:30:00', 3, 5);

-- --------------------------------------------------------

--
-- Table structure for table `Zones`
--

CREATE TABLE `Zones` (
  `z_zoneID` int NOT NULL,
  `zoneName` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Zones`
--

INSERT INTO `Zones` (`z_zoneID`, `zoneName`) VALUES
(1, 'Тренажерный зал'),
(2, 'Бассейн'),
(3, 'Групповые занятия');

-- --------------------------------------------------------

--
-- Table structure for table `ZoneWorkloads`
--

CREATE TABLE `ZoneWorkloads` (
  `workloadID` int NOT NULL,
  `zoneID` int NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `description` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `ZoneWorkloads`
--

INSERT INTO `ZoneWorkloads` (`workloadID`, `zoneID`, `startDate`, `endDate`, `description`) VALUES
(1, 3, '2025-12-15', '2025-12-16', 'Баскетбол');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ClassEnrollments`
--
ALTER TABLE `ClassEnrollments`
  ADD PRIMARY KEY (`enrollmentID`),
  ADD KEY `classID` (`classID`),
  ADD KEY `clientID` (`clientID`);

--
-- Indexes for table `Complaints`
--
ALTER TABLE `Complaints`
  ADD PRIMARY KEY (`complaintID`),
  ADD KEY `clientID` (`clientID`);

--
-- Indexes for table `discount`
--
ALTER TABLE `discount`
  ADD PRIMARY KEY (`discountID`);

--
-- Indexes for table `Equipment`
--
ALTER TABLE `Equipment`
  ADD PRIMARY KEY (`equipmentID`);

--
-- Indexes for table `exercises`
--
ALTER TABLE `exercises`
  ADD PRIMARY KEY (`exerciseID`);

--
-- Indexes for table `GroupClasses`
--
ALTER TABLE `GroupClasses`
  ADD PRIMARY KEY (`classID`),
  ADD KEY `trainerID` (`trainerID`);

--
-- Indexes for table `MembershipFreezes`
--
ALTER TABLE `MembershipFreezes`
  ADD PRIMARY KEY (`freezeID`),
  ADD KEY `mf_membershipID` (`mf_membershipID`);

--
-- Indexes for table `Memberships`
--
ALTER TABLE `Memberships`
  ADD PRIMARY KEY (`membID`),
  ADD KEY `clientID` (`clientID`),
  ADD KEY `adminID` (`adminID`),
  ADD KEY `discountID` (`discountID`);

--
-- Indexes for table `MembershipZones`
--
ALTER TABLE `MembershipZones`
  ADD PRIMARY KEY (`memberzoneID`),
  ADD KEY `mz_membershipID` (`mz_membershipID`),
  ADD KEY `mz_zoneID` (`mz_zoneID`);

--
-- Indexes for table `Notifications`
--
ALTER TABLE `Notifications`
  ADD PRIMARY KEY (`notificationID`),
  ADD KEY `userID` (`userID`);

--
-- Indexes for table `PersExercises`
--
ALTER TABLE `PersExercises`
  ADD PRIMARY KEY (`PersExerciseID`),
  ADD KEY `exerciseID` (`exerciseID`),
  ADD KEY `personaltrainingID` (`personaltrainingID`);

--
-- Indexes for table `PersonalTraining`
--
ALTER TABLE `PersonalTraining`
  ADD PRIMARY KEY (`trainingID`),
  ADD KEY `clientID` (`clientID`),
  ADD KEY `trainerID` (`trainerID`);

--
-- Indexes for table `ProgressMetrics`
--
ALTER TABLE `ProgressMetrics`
  ADD PRIMARY KEY (`metricID`),
  ADD KEY `clientID` (`clientID`),
  ADD KEY `exerciseID` (`exerciseID`);

--
-- Indexes for table `Review`
--
ALTER TABLE `Review`
  ADD PRIMARY KEY (`reviewID`),
  ADD KEY `clientID` (`clientID`);

--
-- Indexes for table `TrainerSpecializations`
--
ALTER TABLE `TrainerSpecializations`
  ADD PRIMARY KEY (`trainer_specialization_id`),
  ADD UNIQUE KEY `trainer_specialization_unique` (`trainerID`,`specialization`),
  ADD KEY `trainerID` (`trainerID`),
  ADD KEY `specialization` (`specialization`);

--
-- Indexes for table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`userID`),
  ADD UNIQUE KEY `login` (`login`);

--
-- Indexes for table `Visits`
--
ALTER TABLE `Visits`
  ADD PRIMARY KEY (`visitID`),
  ADD KEY `clientID` (`clientID`),
  ADD KEY `v_zoneID` (`v_zoneID`),
  ADD KEY `v_membershipID` (`v_membershipID`);

--
-- Indexes for table `Zones`
--
ALTER TABLE `Zones`
  ADD PRIMARY KEY (`z_zoneID`);

--
-- Indexes for table `ZoneWorkloads`
--
ALTER TABLE `ZoneWorkloads`
  ADD PRIMARY KEY (`workloadID`),
  ADD KEY `fk_zoneworkloads_zone` (`zoneID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ClassEnrollments`
--
ALTER TABLE `ClassEnrollments`
  MODIFY `enrollmentID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `Complaints`
--
ALTER TABLE `Complaints`
  MODIFY `complaintID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `discount`
--
ALTER TABLE `discount`
  MODIFY `discountID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `Equipment`
--
ALTER TABLE `Equipment`
  MODIFY `equipmentID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `exercises`
--
ALTER TABLE `exercises`
  MODIFY `exerciseID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `GroupClasses`
--
ALTER TABLE `GroupClasses`
  MODIFY `classID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `MembershipFreezes`
--
ALTER TABLE `MembershipFreezes`
  MODIFY `freezeID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `Memberships`
--
ALTER TABLE `Memberships`
  MODIFY `membID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `MembershipZones`
--
ALTER TABLE `MembershipZones`
  MODIFY `memberzoneID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `Notifications`
--
ALTER TABLE `Notifications`
  MODIFY `notificationID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `PersExercises`
--
ALTER TABLE `PersExercises`
  MODIFY `PersExerciseID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `PersonalTraining`
--
ALTER TABLE `PersonalTraining`
  MODIFY `trainingID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `ProgressMetrics`
--
ALTER TABLE `ProgressMetrics`
  MODIFY `metricID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `Review`
--
ALTER TABLE `Review`
  MODIFY `reviewID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `TrainerSpecializations`
--
ALTER TABLE `TrainerSpecializations`
  MODIFY `trainer_specialization_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `Users`
--
ALTER TABLE `Users`
  MODIFY `userID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `Visits`
--
ALTER TABLE `Visits`
  MODIFY `visitID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `Zones`
--
ALTER TABLE `Zones`
  MODIFY `z_zoneID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `ZoneWorkloads`
--
ALTER TABLE `ZoneWorkloads`
  MODIFY `workloadID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ClassEnrollments`
--
ALTER TABLE `ClassEnrollments`
  ADD CONSTRAINT `classenrollments_ibfk_1` FOREIGN KEY (`classID`) REFERENCES `GroupClasses` (`classID`),
  ADD CONSTRAINT `classenrollments_ibfk_2` FOREIGN KEY (`clientID`) REFERENCES `Users` (`userID`);

--
-- Constraints for table `Complaints`
--
ALTER TABLE `Complaints`
  ADD CONSTRAINT `complaints_ibfk_1` FOREIGN KEY (`clientID`) REFERENCES `Users` (`userID`);

--
-- Constraints for table `GroupClasses`
--
ALTER TABLE `GroupClasses`
  ADD CONSTRAINT `groupclasses_ibfk_1` FOREIGN KEY (`trainerID`) REFERENCES `Users` (`userID`);

--
-- Constraints for table `MembershipFreezes`
--
ALTER TABLE `MembershipFreezes`
  ADD CONSTRAINT `membershipfreezes_ibfk_1` FOREIGN KEY (`mf_membershipID`) REFERENCES `Memberships` (`membID`);

--
-- Constraints for table `Memberships`
--
ALTER TABLE `Memberships`
  ADD CONSTRAINT `memberships_ibfk_1` FOREIGN KEY (`clientID`) REFERENCES `Users` (`userID`),
  ADD CONSTRAINT `memberships_ibfk_2` FOREIGN KEY (`adminID`) REFERENCES `Users` (`userID`),
  ADD CONSTRAINT `memberships_ibfk_3` FOREIGN KEY (`discountID`) REFERENCES `discount` (`discountID`);

--
-- Constraints for table `MembershipZones`
--
ALTER TABLE `MembershipZones`
  ADD CONSTRAINT `membershipzones_ibfk_1` FOREIGN KEY (`mz_membershipID`) REFERENCES `Memberships` (`membID`),
  ADD CONSTRAINT `membershipzones_ibfk_2` FOREIGN KEY (`mz_zoneID`) REFERENCES `Zones` (`z_zoneID`);

--
-- Constraints for table `Notifications`
--
ALTER TABLE `Notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `Users` (`userID`);

--
-- Constraints for table `PersExercises`
--
ALTER TABLE `PersExercises`
  ADD CONSTRAINT `persexercises_ibfk_1` FOREIGN KEY (`exerciseID`) REFERENCES `exercises` (`exerciseID`),
  ADD CONSTRAINT `persexercises_ibfk_2` FOREIGN KEY (`personaltrainingID`) REFERENCES `PersonalTraining` (`trainingID`);

--
-- Constraints for table `PersonalTraining`
--
ALTER TABLE `PersonalTraining`
  ADD CONSTRAINT `personaltraining_ibfk_1` FOREIGN KEY (`clientID`) REFERENCES `Users` (`userID`),
  ADD CONSTRAINT `personaltraining_ibfk_2` FOREIGN KEY (`trainerID`) REFERENCES `Users` (`userID`);

--
-- Constraints for table `ProgressMetrics`
--
ALTER TABLE `ProgressMetrics`
  ADD CONSTRAINT `progressmetrics_ibfk_1` FOREIGN KEY (`clientID`) REFERENCES `Users` (`userID`),
  ADD CONSTRAINT `progressmetrics_ibfk_2` FOREIGN KEY (`exerciseID`) REFERENCES `exercises` (`exerciseID`);

--
-- Constraints for table `Review`
--
ALTER TABLE `Review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`clientID`) REFERENCES `Users` (`userID`);

--
-- Constraints for table `TrainerSpecializations`
--
ALTER TABLE `TrainerSpecializations`
  ADD CONSTRAINT `trainerspecializations_ibfk_1` FOREIGN KEY (`trainerID`) REFERENCES `Users` (`userID`);

--
-- Constraints for table `Visits`
--
ALTER TABLE `Visits`
  ADD CONSTRAINT `visits_ibfk_1` FOREIGN KEY (`clientID`) REFERENCES `Users` (`userID`),
  ADD CONSTRAINT `visits_ibfk_2` FOREIGN KEY (`v_zoneID`) REFERENCES `Zones` (`z_zoneID`),
  ADD CONSTRAINT `visits_ibfk_3` FOREIGN KEY (`v_membershipID`) REFERENCES `Memberships` (`membID`);

--
-- Constraints for table `ZoneWorkloads`
--
ALTER TABLE `ZoneWorkloads`
  ADD CONSTRAINT `fk_zoneworkloads_zone` FOREIGN KEY (`zoneID`) REFERENCES `Zones` (`z_zoneID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
