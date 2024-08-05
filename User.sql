-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               11.4.2-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for user
CREATE DATABASE IF NOT EXISTS `user` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `user`;

-- Dumping structure for table user.anchor
CREATE TABLE IF NOT EXISTS `anchor` (
  `Anchor_ID` int(11) NOT NULL,
  `Anchor_Name` varchar(50) DEFAULT NULL,
  `Room_ID` int(11) DEFAULT NULL,
  `Anchor_Status` enum('Active','Inactive','Unknown') DEFAULT 'Unknown',
  PRIMARY KEY (`Anchor_ID`),
  KEY `FK_anchor_room` (`Room_ID`),
  CONSTRAINT `FK_anchor_room` FOREIGN KEY (`Room_ID`) REFERENCES `room` (`room_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table user.anchor: ~0 rows (approximately)

-- Dumping structure for table user.anchor_history
CREATE TABLE IF NOT EXISTS `anchor_history` (
  `History_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Anchor_ID` int(11) DEFAULT NULL,
  `Anchor_Name` varchar(50) DEFAULT NULL,
  `Room_ID` int(11) DEFAULT NULL,
  `Anchor_Status` enum('Active','Inactive','Unknown') DEFAULT NULL,
  `Change_Date` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`History_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table user.anchor_history: ~0 rows (approximately)

-- Dumping structure for function user.anchor_last_active
DELIMITER //
CREATE FUNCTION `anchor_last_active`(`Given_Anchor_ID` INT
) RETURNS datetime
    READS SQL DATA
BEGIN
    DECLARE last_date DATETIME;

    -- Check if the anchor status is 'active'
    IF EXISTS (
        SELECT 1
        FROM anchor
        WHERE anchor.Anchor_ID = Given_Anchor_ID AND anchor.Anchor_Status = 'active'
    ) THEN
        -- Set last_date to the current date and time
        SET last_date = NOW();
    ELSE
        -- Retrieve the most recent Change_Date where status was 'Active'
        SELECT anchor_history.Change_Date
        INTO last_date
        FROM anchor_history
        WHERE anchor_history.Anchor_ID = Given_Anchor_ID AND anchor_history.Anchor_Status = 'Active'
        ORDER BY anchor_history.Change_Date DESC
        LIMIT 1;
    END IF;

    -- Return the last_date
    RETURN last_date;
END//
DELIMITER ;

-- Dumping structure for table user.card
CREATE TABLE IF NOT EXISTS `card` (
  `Card_ID` int(11) NOT NULL,
  `Card_Name` varchar(250) DEFAULT NULL,
  `Anchor_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`Card_ID`) USING BTREE,
  KEY `FK_card_anchor` (`Anchor_ID`),
  CONSTRAINT `FK_card_anchor` FOREIGN KEY (`Anchor_ID`) REFERENCES `anchor` (`Anchor_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table user.card: ~0 rows (approximately)

-- Dumping structure for table user.company
CREATE TABLE IF NOT EXISTS `company` (
  `Company_ID` int(11) NOT NULL,
  `Company_Name` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`Company_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table user.company: ~0 rows (approximately)

-- Dumping structure for table user.place
CREATE TABLE IF NOT EXISTS `place` (
  `Place_ID` int(11) NOT NULL,
  `Place_Name` varchar(50) DEFAULT NULL,
  `Plant_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`Place_ID`),
  KEY `FK_place_plant` (`Plant_ID`),
  CONSTRAINT `FK_place_plant` FOREIGN KEY (`Plant_ID`) REFERENCES `plant` (`Plant_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table user.place: ~0 rows (approximately)

-- Dumping structure for table user.plant
CREATE TABLE IF NOT EXISTS `plant` (
  `Plant_ID` int(11) NOT NULL,
  `Plant_Name` varchar(250) DEFAULT NULL,
  `Company_ID` int(11) DEFAULT NULL,
  `Server_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`Plant_ID`),
  UNIQUE KEY `Index 4` (`Server_ID`),
  KEY `FK__company` (`Company_ID`),
  CONSTRAINT `FK__company` FOREIGN KEY (`Company_ID`) REFERENCES `company` (`Company_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_plant_server` FOREIGN KEY (`Server_ID`) REFERENCES `server` (`Server_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table user.plant: ~0 rows (approximately)

-- Dumping structure for table user.plant_history
CREATE TABLE IF NOT EXISTS `plant_history` (
  `History_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Plant_ID` int(11) NOT NULL,
  `Plant_Name` varchar(250) DEFAULT NULL,
  `Company_ID` int(11) DEFAULT NULL,
  `Server_ID` int(11) DEFAULT NULL,
  `Change_Date` datetime NOT NULL DEFAULT current_timestamp(),
  `Is_Last` enum('Last') DEFAULT NULL,
  PRIMARY KEY (`History_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci ROW_FORMAT=DYNAMIC;

-- Dumping data for table user.plant_history: ~0 rows (approximately)

-- Dumping structure for table user.room
CREATE TABLE IF NOT EXISTS `room` (
  `room_ID` int(11) NOT NULL,
  `room_Name` varchar(250) DEFAULT NULL,
  `Place_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`room_ID`),
  KEY `FK_room_place` (`Place_ID`),
  CONSTRAINT `FK_room_place` FOREIGN KEY (`Place_ID`) REFERENCES `place` (`Place_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table user.room: ~0 rows (approximately)

-- Dumping structure for table user.room_logs
CREATE TABLE IF NOT EXISTS `room_logs` (
  `Log_ID` int(11) NOT NULL AUTO_INCREMENT,
  `User_ID` int(11) NOT NULL,
  `Room_ID` int(11) NOT NULL,
  `Log_Type` enum('IN','OUT') NOT NULL,
  `Log_Date` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`Log_ID`),
  KEY `FK__user` (`User_ID`),
  KEY `FK__room` (`Room_ID`),
  CONSTRAINT `FK__room` FOREIGN KEY (`Room_ID`) REFERENCES `room` (`room_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK__user` FOREIGN KEY (`User_ID`) REFERENCES `user` (`User_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table user.room_logs: ~0 rows (approximately)

-- Dumping structure for table user.server
CREATE TABLE IF NOT EXISTS `server` (
  `Server_ID` int(11) NOT NULL,
  `Server_Name` varchar(50) DEFAULT NULL,
  `Server_Status` enum('Active','Inactive','Unknown') DEFAULT 'Unknown',
  PRIMARY KEY (`Server_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table user.server: ~0 rows (approximately)

-- Dumping structure for table user.server_history
CREATE TABLE IF NOT EXISTS `server_history` (
  `History_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Server_ID` int(11) DEFAULT NULL,
  `Server_Name` varchar(50) DEFAULT NULL,
  `Server_Status` enum('Active','Inactive','Unknown') DEFAULT NULL,
  `Change_Date` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`History_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table user.server_history: ~0 rows (approximately)

-- Dumping structure for table user.sessions
CREATE TABLE IF NOT EXISTS `sessions` (
  `Session_Code` varchar(24) NOT NULL,
  `User_ID` int(11) NOT NULL DEFAULT 0,
  `Start_Date` datetime NOT NULL DEFAULT current_timestamp(),
  `End_Date` datetime DEFAULT NULL,
  PRIMARY KEY (`Session_Code`),
  KEY `FK1_UserID` (`User_ID`),
  CONSTRAINT `FK1_UserID` FOREIGN KEY (`User_ID`) REFERENCES `user` (`User_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table user.sessions: ~1 rows (approximately)
INSERT INTO `sessions` (`Session_Code`, `User_ID`, `Start_Date`, `End_Date`) VALUES
	('exampleSession', 1, '2024-08-05 15:11:37', NULL);

-- Dumping structure for table user.user
CREATE TABLE IF NOT EXISTS `user` (
  `User_ID` int(11) NOT NULL,
  `username` varchar(250) DEFAULT NULL,
  `password` varchar(250) DEFAULT NULL,
  `email` varchar(250) DEFAULT NULL,
  `session` varchar(250) DEFAULT NULL,
  `Card_ID` int(11) DEFAULT NULL,
  `Company_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`User_ID`) USING BTREE,
  UNIQUE KEY `session` (`session`),
  UNIQUE KEY `device_ID` (`Card_ID`) USING BTREE,
  KEY `FK_user_company` (`Company_ID`),
  CONSTRAINT `FK_user_card` FOREIGN KEY (`Card_ID`) REFERENCES `card` (`Card_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_user_company` FOREIGN KEY (`Company_ID`) REFERENCES `company` (`Company_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table user.user: ~1 rows (approximately)
INSERT INTO `user` (`User_ID`, `username`, `password`, `email`, `session`, `Card_ID`, `Company_ID`) VALUES
	(1, 'exampleUser', 'examplePassword', NULL, 'exampleSession', NULL, NULL);

-- Dumping structure for view user.user_count_in_rooms
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `user_count_in_rooms` (
	`room_ID` INT(11) NOT NULL,
	`count(user.User_ID)` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Dumping structure for trigger user.anchor_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `anchor_before_update` BEFORE UPDATE ON `anchor` FOR EACH ROW BEGIN
    -- Save current data to anchor_history
		INSERT INTO anchor_history (Anchor_ID, Anchor_Name, Room_ID, Anchor_Status)
		VALUES (OLD.anchor_ID, OLD.anchor_Name, OLD.room_ID, OLD.anchor_Status);
    -- The actual update on the anchor table occurs after this trigger
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger user.company_before_delete
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `company_before_delete` BEFORE DELETE ON `company` FOR EACH ROW BEGIN

	UPDATE plant
	SET plant.Company_ID = NULL
	WHERE plant.Company_ID = OLD.Company_ID;
	
	UPDATE user
	SET user.Company_ID = null
	WHERE user.Company_ID = OLD.Company_ID;
	
	
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger user.plant_before_delete
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `plant_before_delete` BEFORE DELETE ON `plant` FOR EACH ROW BEGIN

	UPDATE place
	SET place.Plant_ID = NULL
	WHERE place.Plant_ID = OLD.Plant_ID;
	
	UPDATE server
	SET server.Server_Status = "Unknown"
	WHERE server.Server_ID = OLD.Server_ID;
	
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger user.plant_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `plant_before_update` BEFORE UPDATE ON `plant` FOR EACH ROW BEGIN

		UPDATE plant_history
		SET plant_history.Is_Last = Null
		WHERE plant_history.Plant_ID = OLD.Plant_ID AND plant_history.Is_Last = 'Last';

		INSERT INTO plant_history (plant_history.Plant_ID, plant_history.Plant_Name, plant_history.Company_ID, plant_history.Server_ID, plant_history.Is_Last)
		VALUES (OLD.Plant_ID, OLD.Plant_Name, OLD.Company_ID, OLD.Server_ID, 'Last');
		
		

END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger user.server_after_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `server_after_update` AFTER UPDATE ON `server` FOR EACH ROW BEGIN
    IF NEW.Server_Status IN ('Inactive', 'Unknown') AND NEW.Server_Status != OLD.Server_Status THEN
        UPDATE anchor
        SET Anchor_Status = 'Unknown'
        WHERE Anchor_ID IN (
            SELECT anchor.Anchor_ID
            FROM anchor
            JOIN room ON anchor.Room_ID = room.Room_ID
            JOIN place ON room.Place_ID = place.Place_ID
            JOIN plant ON place.Plant_ID = plant.Plant_ID
            JOIN server ON plant.Server_ID = server.Server_ID
            WHERE server.Server_ID = NEW.Server_ID
        );
    END IF;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger user.server_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `server_before_update` BEFORE UPDATE ON `server` FOR EACH ROW BEGIN
    -- Save current data to anchor_history
		INSERT INTO server_history (Server_ID, Server_Name, Server_Status)
		VALUES (OLD.server_ID, OLD.server_Name, OLD.Server_Status);
    -- The actual update on the anchor table occurs after this trigger
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `user_count_in_rooms`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `user_count_in_rooms` AS SELECT room.room_ID, count(user.User_ID) FROM Room
JOIN anchor ON room.room_ID = anchor.Room_ID
JOIN card ON card.Anchor_ID = anchor.Anchor_ID
JOIN user ON user.Card_ID = card.Card_ID
WHERE user.Card_ID IS NOT NULL
GROUP BY room.room_ID ;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
