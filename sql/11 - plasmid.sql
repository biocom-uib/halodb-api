
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

USE `halodb` ;

-- -----------------------------------------------------
-- Table `halodb`.`plasmid`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`plasmid` ;
CREATE TABLE IF NOT EXISTS `halodb`.`plasmid` (
  `is_public`   BOOLEAN     NULL DEFAULT false  COMMENT "True if the sample is public. That means it can’t be modified. If a sample is made public, it is available for every user and group and for external visitors.",
  `id`  INT     NOT NULL AUTO_INCREMENT COMMENT "Sample unique internal identifier",
  `source_id`   INT     NOT NULL    COMMENT "To which part does the current element belong?",
  `created` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT "Date created",
  `updated` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT "Date updated",
  `user_id` INT     NOT NULL    COMMENT "User",
  `seqdepth`    FLOAT       NULL DEFAULT NULL   COMMENT "Sequencing depth (Isolates/MAG)",
  `hkgn`    INT     NULL DEFAULT NULL   COMMENT "Alternative housekeeping genes",
  `ggcm`    FLOAT       NULL DEFAULT NULL   COMMENT "Molar percentage of Guanine and Cytosine in DNA.",
  `asem`    INT     NULL DEFAULT NULL   COMMENT "Software used for assembly",
  `asftparams`  VARCHAR (80)    NULL DEFAULT NULL   COMMENT "Parameters used with asem",
  `assembled`   VARCHAR (40)    NULL DEFAULT NULL   COMMENT "Identificador del fitxer d’assembled",
  `assname` VARCHAR (100)   NULL DEFAULT NULL   COMMENT "Name of the original file containing the assembly",
  `asize`   INT     NULL DEFAULT NULL   COMMENT "Assembly size in base pairs",
  `contignumber`    INT     NULL DEFAULT NULL   COMMENT "Number of contigs",
  PRIMARY KEY (`id`),
  INDEX `fk_plasmid_predicted_genes_1_idx` (`source_id` ASC),
  CONSTRAINT `fk_plasmid_predicted_genes_1`
    FOREIGN KEY (`source_id`)
    REFERENCES `halodb`.`predicted_genes` (`id`),
  INDEX `fk_plasmid_user_1_idx` (`user_id` ASC),
  CONSTRAINT `fk_plasmid_user_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  INDEX `fk_plasmid_assembly_1_idx` (`asem` ASC),
  CONSTRAINT `fk_plasmid_assembly_1`
    FOREIGN KEY (`id`)
    REFERENCES `halodb`.`assembly` (`id`)
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