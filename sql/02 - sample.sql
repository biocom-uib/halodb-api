
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

USE `halodb` ;

-- -----------------------------------------------------
-- Table `halodb`.`sample`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`sample` ;
CREATE TABLE IF NOT EXISTS `halodb`.`sample` (
  `is_public`   BOOLEAN     NULL DEFAULT false  COMMENT "True if the sample is public. That means it can’t be modified. If a sample is made public, it is available for every user and group and for external visitors.",
  `id`  INT     NOT NULL AUTO_INCREMENT COMMENT "Sample unique internal identifier",
  `project_id`  INT     NULL DEFAULT NULL   COMMENT "Project of the sample",
  `created` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT "Date created",
  `updated` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT "Date updated",
  `user_id` INT     NOT NULL    COMMENT "User",
  `coun`    VARCHAR (30)    NULL DEFAULT NULL   COMMENT "Country of origin",
  `regi`    VARCHAR (30)    NULL DEFAULT NULL   COMMENT "Region of origin",
  `geol`    VARCHAR (80)    NULL DEFAULT NULL   COMMENT "Geographic location",
  `lati`    FLOAT       NULL DEFAULT NULL   COMMENT "Latitude",
  `long`    FLOAT       NULL DEFAULT NULL   COMMENT "Longitude",
  `alti`    FLOAT       NULL DEFAULT NULL   COMMENT "Altitude in meters, over level at sea, where the sample was taken.",
  `dept`    FLOAT       NULL DEFAULT NULL   COMMENT "Depth, in meters, where the sample was taken, with respect to the fild alti. That is, if the sample was taken in a lake placed on a mountain, alti contains the altitude of the lake's surface and dept represents the depth into the lake where the sample was taken.",
  `sour`    VARCHAR (80)    NULL DEFAULT NULL   COMMENT "Source of sample",
  `dats`    DATE        NULL DEFAULT NULL   COMMENT "Sampling date",
  `hocs`    TIME        NULL DEFAULT NULL   COMMENT "Hour of collection of the sample [sharp hours]",
  `name`    VARCHAR (100)   NULL DEFAULT NULL   COMMENT "Sample name",
  `stype`   VARCHAR (200)   NULL DEFAULT NULL   COMMENT "Sample type. Description of the sample",
  `ssize`   FLOAT       NULL DEFAULT NULL   COMMENT "Sample size (weight, volume)",
  `ssizeunit`   ENUM    ("μl","ml","l","g","Kg")    NULL DEFAULT NULL   COMMENT "Units of ssize",
  `target_id`   INT     NULL DEFAULT NULL   COMMENT "Target nucleic acids",
  PRIMARY KEY (`id`),
  INDEX `fk_sample_project_1_idx` (`project_id` ASC),
  CONSTRAINT `fk_sample_project_1`
    FOREIGN KEY (`project_id`)
    REFERENCES `halodb`.`project` (`id`),
  INDEX `fk_sample_user_1_idx` (`user_id` ASC),
  CONSTRAINT `fk_sample_user_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  INDEX `fk_sample_target_1_idx` (`target_id` ASC),
  CONSTRAINT `fk_sample_target_1`
    FOREIGN KEY (`target_id`)
    REFERENCES `halodb`.`target` (`id`)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- -----------------------------------------------------
-- -----------------------------------------------------


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
