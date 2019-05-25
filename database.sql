-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema crypto_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema crypto_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `crypto_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `crypto_db` ;

-- -----------------------------------------------------
-- Table `crypto_db`.`channel`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `crypto_db`.`channel` (
  `entity` INT(11) NOT NULL,
  PRIMARY KEY (`entity`),
  UNIQUE INDEX `entity_UNIQUE` (`entity` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `crypto_db`.`channel_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `crypto_db`.`channel_user` (
  `id_user` INT(11) NOT NULL,
  `type` INT(11) NOT NULL,
  `id_channel` INT(11) NOT NULL,
  PRIMARY KEY (`id_user`, `id_channel`),
  INDEX `fk_channel_idx` (`id_channel` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `crypto_db`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `crypto_db`.`user` (
  `entity` INT(11) NOT NULL,
  `last_forward` INT(11) NULL DEFAULT NULL,
  `start` TINYINT(4) NULL DEFAULT '0',
  PRIMARY KEY (`entity`),
  UNIQUE INDEX `entity_UNIQUE` (`entity` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `crypto_db`.`filter`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `crypto_db`.`filter` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `id_user` INT(11) NOT NULL,
  `text` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `user_filter_fk_idx` (`id_user` ASC) VISIBLE,
  CONSTRAINT `user_filter_fk`
    FOREIGN KEY (`id_user`)
    REFERENCES `crypto_db`.`user` (`entity`))
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `crypto_db`.`puppet`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `crypto_db`.`puppet` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `entity` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `entity_UNIQUE` (`entity` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
