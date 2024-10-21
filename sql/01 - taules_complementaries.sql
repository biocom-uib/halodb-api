-- MySQL Script generated by MySQL Workbench
-- Thu May 30 09:04:39 2024
-- Model: General    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema halodb
-- -----------------------------------------------------

USE `halodb` ;


-- -----------------------------------------------------
-- Table `halodb`.`hkgenes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`hkgenes` ;

CREATE TABLE IF NOT EXISTS `halodb`.`hkgenes` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT 'Identification of a housekeeping gene',
  `gene` VARCHAR(25) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_bin' NULL DEFAULT NULL COMMENT 'table of generic genes. To be used as housekeeping genes.',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`keywords`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`keywords` ;

CREATE TABLE IF NOT EXISTS `halodb`.`keywords` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `keyword` VARCHAR(50) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
    PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;



-- -----------------------------------------------------
-- Table `halodb`.`assembly`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`assembly` ;

CREATE TABLE IF NOT EXISTS `halodb`.`assembly` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL COMMENT 'Software used for assembly',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`binning`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`binning` ;

CREATE TABLE IF NOT EXISTS `halodb`.`binning` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL COMMENT 'Binning software used',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`fraction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`fraction` ;

CREATE TABLE IF NOT EXISTS `halodb`.`fraction` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`extraction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`extraction` ;

CREATE TABLE IF NOT EXISTS `halodb`.`extraction` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(40) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL COMMENT 'DNA extraction method',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;




-- -----------------------------------------------------
-- Table `halodb`.`method`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`method` ;

CREATE TABLE IF NOT EXISTS `halodb`.`method` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `halodb`.`sequencing`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`sequencing` ;

CREATE TABLE IF NOT EXISTS `halodb`.`sequencing` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`oxygen`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`oxygen` ;

CREATE TABLE IF NOT EXISTS `halodb`.`oxygen` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`target`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`target` ;

CREATE TABLE IF NOT EXISTS `halodb`.`target` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`ph`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`ph` ;

CREATE TABLE IF NOT EXISTS `halodb`.`ph` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(40) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `vmin` FLOAT(11) NULL DEFAULT NULL,
  `vmax` FLOAT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`temperature`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`temperature` ;

CREATE TABLE IF NOT EXISTS `halodb`.`temperature` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(40) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `vmin` FLOAT(11) NULL DEFAULT NULL,
  `vmax` FLOAT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`salinity`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`salinity` ;

CREATE TABLE IF NOT EXISTS `halodb`.`salinity` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(40) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `vmin` FLOAT(11) NULL DEFAULT NULL,
  `vmax` FLOAT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ------------------------------------------------------------------------
-- ------------------------------------------------------------------------
-- ------------------------------------------------------------------------
-- ------------------------------------------------------------------------


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
