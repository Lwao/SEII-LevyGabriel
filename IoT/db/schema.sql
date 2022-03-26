CREATE DATABASE iotdashboard;
USE iotdashboard;

CREATE TABLE `iotdashboard`.`users` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`username` VARCHAR(255),
	`password` VARCHAR(255),
	PRIMARY KEY (ID));