-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema supernovashaman
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema supernovashaman
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `supernovashaman` DEFAULT CHARACTER SET utf8 ;
USE `supernovashaman` ;

-- -----------------------------------------------------
-- Table `supernovashaman`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `supernovashaman`.`users` ;

CREATE TABLE IF NOT EXISTS `supernovashaman`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(64) NULL,
  `email` VARCHAR(120) NULL,
  `password_hash` VARCHAR(256) NULL,
  `name_first` VARCHAR(64) NULL,
  `name_last` VARCHAR(64) NULL,
  `registered_on` DATETIME NULL DEFAULT NOW(),
  `last_seen` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `supernovashaman`.`cards`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `supernovashaman`.`cards` ;

CREATE TABLE IF NOT EXISTS `supernovashaman`.`cards` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(32) NULL,
  `description` VARCHAR(1024) NULL,
  `type` VARCHAR(16) NULL,
  `released_on` DATETIME NULL,
  `status` VARCHAR(16) NULL,
  `quantity` INT NULL,
  `filename` VARCHAR(128) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `supernovashaman`.`favorite`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `supernovashaman`.`favorite` ;

CREATE TABLE IF NOT EXISTS `supernovashaman`.`favorite` (
  `user_id` INT NOT NULL,
  `card_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `card_id`),
  INDEX `fk_user_has_card_card1_idx` (`card_id` ASC) VISIBLE,
  INDEX `fk_user_has_card_user_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_user_has_card_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `supernovashaman`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_has_card_card1`
    FOREIGN KEY (`card_id`)
    REFERENCES `supernovashaman`.`cards` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
