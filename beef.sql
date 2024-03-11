CREATE DATABASE `ApiaristBase`;
USE `ApiaristBase`; 

DROP TABLE IF EXISTS `apiarist`;
CREATE TABLE `apiarist` (
  `aid` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(200) DEFAULT NULL,
  `lastName` VARCHAR(200) DEFAULT NULL,
  `addRess` VARCHAR(200) DEFAULT NULL,
  `email` VARCHAR(200) DEFAULT NULL,
  `phone` VARCHAR(200) DEFAULT NULL,
  `state` VARCHAR(50) DEFAULT NULL,
  `date` TIMESTAMP DEFAULT NOW(),
  `userName` VARCHAR(200) NOT NULL,
  `password` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`aid`)
) ENGINE=INNODB  DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `employee`;
CREATE TABLE `employee` (
  `eid` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(200) NOT NULL,
  `lastName` VARCHAR(200) NOT NULL,
  `userName` VARCHAR(200) NOT NULL,
  `password` VARCHAR(200) NOT NULL,
  `email` VARCHAR(200) NOT NULL,
  `phone` VARCHAR(200) NOT NULL,
  `position` VARCHAR(200) NOT NULL,
  `department` VARCHAR(200) NOT NULL,
  `state` VARCHAR(50) NOT NULL,
  `date` TIMESTAMP NOT NULL,
  `role` TINYINT(1) NOT NULL,
  PRIMARY KEY (`eid`)
) ENGINE=INNODB  DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `guide`;
CREATE TABLE `guide` (
  `gid` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(200) NOT NULL,
  `exist` TINYINT(1) NOT NULL,
  `commonName` VARCHAR(200) NOT NULL,
  `scientificName` VARCHAR(200) NOT NULL,
  `mainFeatures` VARCHAR(200) NOT NULL,
  `description` VARCHAR(200) NOT NULL,
  `symptoms` VARCHAR(200) NOT NULL, 
  `images` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`gid`)
) ENGINE=INNODB  DEFAULT CHARSET=utf8;

INSERT INTO `employee`(firstName,lastName,userName,`password`,email,phone,`position`,department,state,`date`,`role`)VALUES('Ling','Hai','admin','pbkdf2:sha256:600000$wmLAF7DhaN0KuCS0$05022f8c795bdb4d6032bfec97775cbc102cbb3d81bc00e1001024fcd2144daa','4432@gamil.com','01-222222','admin','Boos','Active',NOW(),1)