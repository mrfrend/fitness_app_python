-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Дек 14 2025 г., 11:35
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `fitness`
--

-- --------------------------------------------------------

--
-- Структура таблицы `ClassEnrollments`
--

CREATE TABLE `ClassEnrollments` (
  `enrollmentID` int NOT NULL,
  `classID` int NOT NULL,
  `clientID` int NOT NULL,
  `status` enum('Enrolled','Canceled','Attended','Absent') DEFAULT 'Enrolled'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `Complaints`
--

CREATE TABLE `Complaints` (
  `complaintID` int NOT NULL,
  `clientID` int NOT NULL,
  `complaintDate` date NOT NULL,
  `text` varchar(250) NOT NULL,
  `status` enum('New','InProgress','Closed') DEFAULT 'New'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `discount`
--

CREATE TABLE `discount` (
  `discountID` int NOT NULL,
  `percentage_disc` decimal(5,2) NOT NULL,
  `dateStart` date NOT NULL,
  `dateEnd` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `Equipment`
--

CREATE TABLE `Equipment` (
  `equipmentID` int NOT NULL,
  `name_e` varchar(100) NOT NULL,
  `quantityExist` int NOT NULL,
  `quantityLeft` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `exercises`
--

CREATE TABLE `exercises` (
  `exerciseID` int NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `GroupClasses`
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

-- --------------------------------------------------------

--
-- Структура таблицы `MembershipFreezes`
--

CREATE TABLE `MembershipFreezes` (
  `freezeID` int NOT NULL,
  `mf_membershipID` int NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `Memberships`
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

-- --------------------------------------------------------

--
-- Структура таблицы `MembershipZones`
--

CREATE TABLE `MembershipZones` (
  `memberzoneID` int NOT NULL,
  `mz_membershipID` int NOT NULL,
  `mz_zoneID` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `Notifications`
--

CREATE TABLE `Notifications` (
  `notificationID` int NOT NULL,
  `userID` int NOT NULL,
  `message_n` varchar(250) NOT NULL,
  `sentDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `status_n` enum('Unread','Read') DEFAULT 'Unread'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `PersExercises`
--

CREATE TABLE `PersExercises` (
  `PersExerciseID` int NOT NULL,
  `exerciseID` int DEFAULT NULL,
  `personaltrainingID` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `PersonalTraining`
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

-- --------------------------------------------------------

--
-- Структура таблицы `ProgressMetrics`
--

CREATE TABLE `ProgressMetrics` (
  `metricID` int NOT NULL,
  `clientID` int NOT NULL,
  `metricDate` date NOT NULL,
  `weight` decimal(5,2) DEFAULT NULL,
  `exerciseID` int DEFAULT NULL,
  `notes` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `Review`
--

CREATE TABLE `Review` (
  `reviewID` int NOT NULL,
  `reviewType` enum('Complaint','Suggestion') DEFAULT NULL,
  `dataRev` datetime DEFAULT CURRENT_TIMESTAMP,
  `textRev` text NOT NULL,
  `clientID` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `TrainerSpecializations`
--

CREATE TABLE `TrainerSpecializations` (
  `trainer_specialization_id` int NOT NULL,
  `trainerID` int NOT NULL,
  `specialization` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `Users`
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

-- --------------------------------------------------------

--
-- Структура таблицы `Visits`
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

-- --------------------------------------------------------

--
-- Структура таблицы `Zones`
--

CREATE TABLE `Zones` (
  `z_zoneID` int NOT NULL,
  `zoneName` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `ClassEnrollments`
--
ALTER TABLE `ClassEnrollments`
  ADD PRIMARY KEY (`enrollmentID`),
  ADD KEY `classID` (`classID`),
  ADD KEY `clientID` (`clientID`);

--
-- Индексы таблицы `Complaints`
--
ALTER TABLE `Complaints`
  ADD PRIMARY KEY (`complaintID`),
  ADD KEY `clientID` (`clientID`);

--
-- Индексы таблицы `discount`
--
ALTER TABLE `discount`
  ADD PRIMARY KEY (`discountID`);

--
-- Индексы таблицы `Equipment`
--
ALTER TABLE `Equipment`
  ADD PRIMARY KEY (`equipmentID`);

--
-- Индексы таблицы `exercises`
--
ALTER TABLE `exercises`
  ADD PRIMARY KEY (`exerciseID`);

--
-- Индексы таблицы `GroupClasses`
--
ALTER TABLE `GroupClasses`
  ADD PRIMARY KEY (`classID`),
  ADD KEY `trainerID` (`trainerID`);

--
-- Индексы таблицы `MembershipFreezes`
--
ALTER TABLE `MembershipFreezes`
  ADD PRIMARY KEY (`freezeID`),
  ADD KEY `mf_membershipID` (`mf_membershipID`);

--
-- Индексы таблицы `Memberships`
--
ALTER TABLE `Memberships`
  ADD PRIMARY KEY (`membID`),
  ADD KEY `clientID` (`clientID`),
  ADD KEY `adminID` (`adminID`),
  ADD KEY `discountID` (`discountID`);

--
-- Индексы таблицы `MembershipZones`
--
ALTER TABLE `MembershipZones`
  ADD PRIMARY KEY (`memberzoneID`),
  ADD KEY `mz_membershipID` (`mz_membershipID`),
  ADD KEY `mz_zoneID` (`mz_zoneID`);

--
-- Индексы таблицы `Notifications`
--
ALTER TABLE `Notifications`
  ADD PRIMARY KEY (`notificationID`),
  ADD KEY `userID` (`userID`);

--
-- Индексы таблицы `PersExercises`
--
ALTER TABLE `PersExercises`
  ADD PRIMARY KEY (`PersExerciseID`),
  ADD KEY `exerciseID` (`exerciseID`),
  ADD KEY `personaltrainingID` (`personaltrainingID`);

--
-- Индексы таблицы `PersonalTraining`
--
ALTER TABLE `PersonalTraining`
  ADD PRIMARY KEY (`trainingID`),
  ADD KEY `clientID` (`clientID`),
  ADD KEY `trainerID` (`trainerID`);

--
-- Индексы таблицы `ProgressMetrics`
--
ALTER TABLE `ProgressMetrics`
  ADD PRIMARY KEY (`metricID`),
  ADD KEY `clientID` (`clientID`),
  ADD KEY `exerciseID` (`exerciseID`);

--
-- Индексы таблицы `Review`
--
ALTER TABLE `Review`
  ADD PRIMARY KEY (`reviewID`),
  ADD KEY `clientID` (`clientID`);

--
-- Индексы таблицы `TrainerSpecializations`
--
ALTER TABLE `TrainerSpecializations`
  ADD PRIMARY KEY (`trainer_specialization_id`),
  ADD UNIQUE KEY `trainer_specialization_unique` (`trainerID`, `specialization`),
  ADD KEY `trainerID` (`trainerID`),
  ADD KEY `specialization` (`specialization`);

--
-- Индексы таблицы `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`userID`),
  ADD UNIQUE KEY `login` (`login`);

--
-- Индексы таблицы `Visits`
--
ALTER TABLE `Visits`
  ADD PRIMARY KEY (`visitID`),
  ADD KEY `clientID` (`clientID`),
  ADD KEY `v_zoneID` (`v_zoneID`),
  ADD KEY `v_membershipID` (`v_membershipID`);

--
-- Индексы таблицы `Zones`
--
ALTER TABLE `Zones`
  ADD PRIMARY KEY (`z_zoneID`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `ClassEnrollments`
--
ALTER TABLE `ClassEnrollments`
  MODIFY `enrollmentID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Complaints`
--
ALTER TABLE `Complaints`
  MODIFY `complaintID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `discount`
--
ALTER TABLE `discount`
  MODIFY `discountID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Equipment`
--
ALTER TABLE `Equipment`
  MODIFY `equipmentID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `exercises`
--
ALTER TABLE `exercises`
  MODIFY `exerciseID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `GroupClasses`
--
ALTER TABLE `GroupClasses`
  MODIFY `classID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `MembershipFreezes`
--
ALTER TABLE `MembershipFreezes`
  MODIFY `freezeID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Memberships`
--
ALTER TABLE `Memberships`
  MODIFY `membID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `MembershipZones`
--
ALTER TABLE `MembershipZones`
  MODIFY `memberzoneID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Notifications`
--
ALTER TABLE `Notifications`
  MODIFY `notificationID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `PersExercises`
--
ALTER TABLE `PersExercises`
  MODIFY `PersExerciseID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `PersonalTraining`
--
ALTER TABLE `PersonalTraining`
  MODIFY `trainingID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `ProgressMetrics`
--
ALTER TABLE `ProgressMetrics`
  MODIFY `metricID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Review`
--
ALTER TABLE `Review`
  MODIFY `reviewID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `TrainerSpecializations`
--
ALTER TABLE `TrainerSpecializations`
  MODIFY `trainer_specialization_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Users`
--
ALTER TABLE `Users`
  MODIFY `userID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Visits`
--
ALTER TABLE `Visits`
  MODIFY `visitID` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Zones`
--
ALTER TABLE `Zones`
  MODIFY `z_zoneID` int NOT NULL AUTO_INCREMENT;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `ClassEnrollments`
--
ALTER TABLE `ClassEnrollments`
  ADD CONSTRAINT `classenrollments_ibfk_1` FOREIGN KEY (`classID`) REFERENCES `GroupClasses` (`classID`),
  ADD CONSTRAINT `classenrollments_ibfk_2` FOREIGN KEY (`clientID`) REFERENCES `Users` (`userID`);

--
-- Ограничения внешнего ключа таблицы `Complaints`
--
ALTER TABLE `Complaints`
  ADD CONSTRAINT `complaints_ibfk_1` FOREIGN KEY (`clientID`) REFERENCES `Users` (`userID`);

--
-- Ограничения внешнего ключа таблицы `GroupClasses`
--
ALTER TABLE `GroupClasses`
  ADD CONSTRAINT `groupclasses_ibfk_1` FOREIGN KEY (`trainerID`) REFERENCES `Users` (`userID`);

--
-- Ограничения внешнего ключа таблицы `MembershipFreezes`
--
ALTER TABLE `MembershipFreezes`
  ADD CONSTRAINT `membershipfreezes_ibfk_1` FOREIGN KEY (`mf_membershipID`) REFERENCES `Memberships` (`membID`);

--
-- Ограничения внешнего ключа таблицы `Memberships`
--
ALTER TABLE `Memberships`
  ADD CONSTRAINT `memberships_ibfk_1` FOREIGN KEY (`clientID`) REFERENCES `Users` (`userID`),
  ADD CONSTRAINT `memberships_ibfk_2` FOREIGN KEY (`adminID`) REFERENCES `Users` (`userID`),
  ADD CONSTRAINT `memberships_ibfk_3` FOREIGN KEY (`discountID`) REFERENCES `discount` (`discountID`);

--
-- Ограничения внешнего ключа таблицы `MembershipZones`
--
ALTER TABLE `MembershipZones`
  ADD CONSTRAINT `membershipzones_ibfk_1` FOREIGN KEY (`mz_membershipID`) REFERENCES `Memberships` (`membID`),
  ADD CONSTRAINT `membershipzones_ibfk_2` FOREIGN KEY (`mz_zoneID`) REFERENCES `Zones` (`z_zoneID`);

--
-- Ограничения внешнего ключа таблицы `Notifications`
--
ALTER TABLE `Notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `Users` (`userID`);

--
-- Ограничения внешнего ключа таблицы `PersExercises`
--
ALTER TABLE `PersExercises`
  ADD CONSTRAINT `persexercises_ibfk_1` FOREIGN KEY (`exerciseID`) REFERENCES `exercises` (`exerciseID`),
  ADD CONSTRAINT `persexercises_ibfk_2` FOREIGN KEY (`personaltrainingID`) REFERENCES `PersonalTraining` (`trainingID`);

--
-- Ограничения внешнего ключа таблицы `PersonalTraining`
--
ALTER TABLE `PersonalTraining`
  ADD CONSTRAINT `personaltraining_ibfk_1` FOREIGN KEY (`clientID`) REFERENCES `Users` (`userID`),
  ADD CONSTRAINT `personaltraining_ibfk_2` FOREIGN KEY (`trainerID`) REFERENCES `Users` (`userID`);

--
-- Ограничения внешнего ключа таблицы `ProgressMetrics`
--
ALTER TABLE `ProgressMetrics`
  ADD CONSTRAINT `progressmetrics_ibfk_1` FOREIGN KEY (`clientID`) REFERENCES `Users` (`userID`),
  ADD CONSTRAINT `progressmetrics_ibfk_2` FOREIGN KEY (`exerciseID`) REFERENCES `exercises` (`exerciseID`);

--
-- Ограничения внешнего ключа таблицы `Review`
--
ALTER TABLE `Review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`clientID`) REFERENCES `Users` (`userID`);

--
-- Ограничения внешнего ключа таблицы `TrainerSpecializations`
--
ALTER TABLE `TrainerSpecializations`
  ADD CONSTRAINT `trainerspecializations_ibfk_1` FOREIGN KEY (`trainerID`) REFERENCES `Users` (`userID`);

--
-- Ограничения внешнего ключа таблицы `Visits`
--
ALTER TABLE `Visits`
  ADD CONSTRAINT `visits_ibfk_1` FOREIGN KEY (`clientID`) REFERENCES `Users` (`userID`),
  ADD CONSTRAINT `visits_ibfk_2` FOREIGN KEY (`v_zoneID`) REFERENCES `Zones` (`z_zoneID`),
  ADD CONSTRAINT `visits_ibfk_3` FOREIGN KEY (`v_membershipID`) REFERENCES `Memberships` (`membID`);

INSERT INTO `discount` (`discountID`, `percentage_disc`, `dateStart`, `dateEnd`) VALUES
 (1, 10.00, '2024-06-01', '2024-06-30'),
 (2, 15.00, '2024-01-01', '2024-12-31'),
 (3, 5.00, '2024-06-15', '2024-06-30');

INSERT INTO `Zones` (`z_zoneID`, `zoneName`) VALUES
 (1, 'Тренажерный зал'),
 (2, 'Бассейн'),
 (3, 'Групповые занятия');

INSERT INTO `Users` (`userID`, `first_name`, `last_name`, `middle_name`, `phone`, `email`, `health_limits`, `login`, `password`, `userType`, `birthDate`) VALUES
 (1, 'Марина', 'Сидорова', 'Петровна', '89219014567', 'director@fitness.ru', 'Нет', 'director1', 'pass1', 'Director', '1980-05-15'),
 (2, 'Анна', 'Романова', 'Сергеевна', '89210125678', 'admin1@fitness.ru', 'Нет', 'admin1', 'pass2', 'Administrator', '1992-08-22'),
 (4, 'Елена', 'Яковлева', 'Викторовна', '89211236789', 'admin2@fitness.ru', 'Нет', 'admin2', 'pass3', 'Administrator', '1988-11-10'),
 (7, 'Дмитрий', 'Петров', 'Александрович', '89212347890', 'petrov@fitness.ru', 'Ограничение: травма плеча (небольшие веса)', 'trainer1', 'pass4', 'Trainer', '1985-03-18'),
 (9, 'Ольга', 'Смирнова', 'Игоревна', '89213458901', 'smirnova@fitness.ru', 'Нет', 'trainer2', 'pass5', 'Trainer', '1990-07-25'),
 (11, 'Сергей', 'Козлов', 'Николаевич', '89214569012', 'kozlov@fitness.ru', 'Нет', 'trainer3', 'pass6', 'Trainer', '1987-12-05'),
 (16, 'Екатерина', 'Федорова', 'Дмитриевна', '89161112236', 'fedorova@mail.ru', 'Ограничение: колено (без прыжков)', 'client1', 'pass7', 'Client', '1995-04-12'),
 (21, 'Алексей', 'Михайлов', 'Владимирович', '89162223347', 'mikhailov@gmail.com', 'Нет', 'client2', 'pass8', 'Client', '1988-09-30'),
 (26, 'Ирина', 'Новикова', 'Сергеевна', '89163334458', 'novikova@yandex.ru', 'Нет', 'client3', 'pass9', 'Client', '1992-06-18'),
 (30, 'Игорь', 'Соколов', 'Петрович', '89164445569', 'sokolov@mail.ru', 'Ограничение: давление (умеренная нагрузка)', 'client4', 'pass10', 'Client', '1983-02-28'),
 (34, 'Мария', 'Павлова', 'Александровна', '89165556670', 'pavlova@gmail.com', 'Нет', 'client5', 'pass11', 'Client', '1997-11-07');

INSERT INTO `TrainerSpecializations` (`trainerID`, `specialization`) VALUES
 (7, 'Силовые тренировки'),
 (7, 'Бокс'),
 (9, 'Йога'),
 (9, 'Пилатес'),
 (11, 'Плавание');

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

INSERT INTO `Memberships` (`membID`, `clientID`, `membType`, `startDate`, `endDate`, `visitsTotal`, `visitsUsed`, `membStatus`, `cost`, `discountID`, `adminID`) VALUES
 (1, 16, 'Месячный безлимит', '2024-06-01', '2024-06-30', 999, 42, 'Active', 5000.00, NULL, 2),
 (2, 21, '12 посещений', '2024-06-05', '2024-09-05', 12, 8, 'Active', 4000.00, NULL, 2),
 (3, 26, 'Годовой VIP', '2024-01-10', '2025-01-10', 999, 156, 'Active', 45000.00, NULL, 4),
 (4, 30, 'Разовое посещение', '2024-06-15', '2024-06-15', 1, 1, 'Completed', 500.00, NULL, 2),
 (5, 34, 'Квартальный', '2024-06-01', '2024-08-31', 999, 15, 'Active', 12000.00, NULL, 4);

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

INSERT INTO `GroupClasses` (`classID`, `className`, `trainerID`, `classDate`, `startTime`, `endTime`, `hall`, `maxParticipants`, `current_participants`, `classStatus`) VALUES
 (1, 'Йога для начинающих', 9, '2024-06-16', '10:00:00', '11:00:00', 'Зал 2', 15, 12, 'Scheduled'),
 (2, 'Силовая аэробика', 7, '2024-06-16', '18:00:00', '19:00:00', 'Зал 1', 20, 18, 'Scheduled'),
 (3, 'Пилатес', 9, '2024-06-17', '11:00:00', '12:00:00', 'Зал 2', 12, 12, 'Full'),
 (4, 'Аквааэробика', 11, '2024-06-17', '15:00:00', '16:00:00', 'Бассейн', 10, 7, 'Scheduled'),
 (5, 'Бокс', 7, '2024-06-18', '19:00:00', '20:30:00', 'Зал 3', 8, 5, 'Scheduled');

INSERT INTO `Visits` (`visitID`, `clientID`, `visitDate`, `checkInTime`, `checkOutTime`, `v_zoneID`, `v_membershipID`) VALUES
 (1, 16, '2024-06-15', '08:30:00', '10:15:00', 1, 1),
 (2, 21, '2024-06-15', '09:00:00', '10:30:00', 1, 2),
 (3, 26, '2024-06-15', '07:00:00', '08:30:00', 2, 3),
 (4, 16, '2024-06-15', '18:00:00', '19:45:00', 3, 1),
 (5, 34, '2024-06-15', '19:00:00', '20:30:00', 3, 5);

INSERT INTO `PersonalTraining` (`trainingID`, `clientID`, `trainerID`, `goalTraining`, `trainingDate`, `startTime`, `endTime`, `notes`) VALUES
 (1, 26, 7, 'Набор мышечной массы', '2024-06-14', '16:00:00', '17:00:00', 'Хорошая техника'),
 (2, 16, 9, 'Гибкость и осанка', '2024-06-13', '10:00:00', '11:00:00', 'Улучшилась гибкость'),
 (3, 21, 7, 'Силовая подготовка', '2024-06-12', '14:00:00', '15:00:00', 'Нужно работать над техникой');

INSERT INTO `PersExercises` (`PersExerciseID`, `exerciseID`, `personaltrainingID`) VALUES
 (1, 1, 1),
 (2, 2, 1),
 (3, 3, 1),
 (4, 4, 2),
 (5, 5, 2),
 (6, 6, 3),
 (7, 7, 3);

INSERT INTO `ProgressMetrics` (`metricID`, `clientID`, `metricDate`, `weight`, `exerciseID`, `notes`) VALUES
 (1, 26, '2024-06-14', 72.50, 1, 'Жим 80кг x 8'),
 (2, 21, '2024-06-12', 83.00, 6, 'Становая 60кг x 6'),
 (3, 16, '2024-06-13', 60.00, 5, 'Растяжка: 15 минут'),
 (4, 34, '2024-06-15', 55.50, NULL, 'Общее самочувствие хорошее');

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
 (10, 5, 34, 'Enrolled');

INSERT INTO `Complaints` (`complaintID`, `clientID`, `complaintDate`, `text`, `status`) VALUES
 (1, 16, '2024-06-15', 'Слишком холодно в зале 2 во время занятий.', 'InProgress'),
 (2, 30, '2024-06-15', 'Не работал один из кардиотренажеров.', 'New'),
 (3, 34, '2024-06-16', 'Хотелось бы больше вечерних занятий по йоге.', 'Closed');

INSERT INTO `Review` (`reviewID`, `reviewType`, `dataRev`, `textRev`, `clientID`) VALUES
 (1, 'Suggestion', '2024-06-16 09:30:00', 'Добавьте, пожалуйста, возможность видеть свободные места в группах.', 21),
 (2, 'Complaint', '2024-06-15 20:45:00', 'Очередь на ресепшене в вечернее время.', 34);

INSERT INTO `Notifications` (`notificationID`, `userID`, `message_n`, `sentDate`, `status_n`) VALUES
 (1, 16, 'Напоминание: у вас занятие "Йога для начинающих" 2024-06-16 в 10:00.', '2024-06-16 08:00:00', 'Unread'),
 (2, 21, 'Напоминание: персональная тренировка 2024-06-12 в 14:00.', '2024-06-12 11:00:00', 'Read'),
 (3, 34, 'Вы записаны на занятие "Бокс" 2024-06-18 в 19:00.', '2024-06-17 12:00:00', 'Unread');

INSERT INTO `Equipment` (`equipmentID`, `name_e`, `quantityExist`, `quantityLeft`) VALUES
 (1, 'Гантели (набор)', 40, 6),
 (2, 'Штанги', 10, 2),
 (3, 'Коврики для йоги', 30, 5),
 (4, 'Скакалки', 20, 8),
 (5, 'Пояса тяжелоатлетические', 8, 1);

INSERT INTO `MembershipFreezes` (`freezeID`, `mf_membershipID`, `startDate`, `endDate`) VALUES
 (1, 1, '2024-06-10', '2024-06-12');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
