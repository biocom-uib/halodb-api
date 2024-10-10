
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

USE `halodb` ;

-- -----------------------------------------------------
-- Table `halodb`.`predicted_genes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`predicted_genes` ;
CREATE TABLE IF NOT EXISTS `halodb`.`predicted_genes` (
  `is_public`   BOOLEAN     NULL DEFAULT false  COMMENT "True if the sample is public. That means it can’t be modified. If a sample is made public, it is available for every user and group and for external visitors.",
  `id`  INT     NOT NULL AUTO_INCREMENT COMMENT "Sample unique internal identifier",
  `source_id`   INT     NOT NULL    COMMENT "To which part does the current element belong?",
  `created` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT "Date created",
  `updated` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT "Date updated",
  `user_id` INT     NOT NULL    COMMENT "User",
  `pgenes`  VARCHAR (40)    NULL DEFAULT NULL   COMMENT "Predicted genes",
  `pgenesname`  VARCHAR (100)   NULL DEFAULT NULL   COMMENT "Name of the original file containing the predicted genes",
  PRIMARY KEY (`id`),
  INDEX `fk_predicted_genes_experiment_1_idx` (`source_id` ASC),
  CONSTRAINT `fk_predicted_genes_experiment_1`
    FOREIGN KEY (`source_id`)
    REFERENCES `halodb`.`experiment` (`id`),
  INDEX `fk_predicted_genes_user_1_idx` (`user_id` ASC),
  CONSTRAINT `fk_predicted_genes_user_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`)
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
