DROP SCHEMA IF EXISTS `Who_Pays_What`;    
CREATE SCHEMA `Who_Pays_What`;
USE `Who_Pays_What`;

CREATE TABLE `Participant`(
	`participantId` INT NOT NULL AUTO_INCREMENT,	
    `firstname` VARCHAR(50),
    `lastname` VARCHAR(100),
	`emailaddress` VARCHAR(250),
    `isOrganizer` BIT,
    `telephonenumber` VARCHAR(15),
    'password_hash' VARCHAR(255),    
    PRIMARY KEY(`participantId`)
);


CREATE TABLE `Event`(
	`eventId` INT NOT NULL AUTO_INCREMENT,
    `description` VARCHAR(100) NOT NULL,
    `eventDate` DATETIME,
    `creationDate` DATETIME,        
    `participantId` INT NOT NULL,
    `isExpired` BIT,    
    `totalAmount` DOUBLE,
    `paidAmount` DOUBLE,
    PRIMARY KEY(`eventId`),
    FOREIGN KEY(`participantId`) REFERENCES `Participant`(`participantId`)
);


CREATE TABLE `ParticipantEvent`(
	`ParticipantEventId` INT NOT NULL AUTO_INCREMENT,
    `eventId` INT NOT NULL,
    `participantId` INT,    
    PRIMARY KEY(`ParticipantEventId`),
    FOREIGN KEY (`eventId`) REFERENCES `Event`(`eventId`),
    FOREIGN KEY(`participantId`) REFERENCES `Participant`(`participantId`) 
);

CREATE TABLE `TransactionType`(
	`typeId` VARCHAR(1) NOT NULL,
    `description` VARCHAR(50),
    PRIMARY KEY (`typeId`)
);

INSERT INTO `TransactionType`(`typeId`, `description`) VALUES('U', 'Uitgave');
INSERT INTO `TransactionType`(`typeId`, `description`) VALUES('P', 'Betalen');
    
CREATE TABLE `Expenditure`(
	`expenditureId` INT NOT NULL AUTO_INCREMENT,
    `ParticipantEventId` INT,
    `description` varchar(50),
    `amount` DOUBLE, 
    `transactionTypeId` varchar(1) NOT NULL,
    `isPaid` BIT,
    PRIMARY KEY (`expenditureId`),
    FOREIGN KEY(`ParticipantEventId`) REFERENCES `ParticipantEvent`(`ParticipantEventId`),
    FOREIGN KEY(`transactionTypeId`) REFERENCES `TransactionType`(`typeId`) 
)