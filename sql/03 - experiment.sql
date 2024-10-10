
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

USE `halodb` ;

-- -----------------------------------------------------
-- Table `halodb`.`experiment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`experiment` ;
CREATE TABLE IF NOT EXISTS `halodb`.`experiment` (
  `is_public`   BOOLEAN     NULL DEFAULT false  COMMENT "True if the sample is public. That means it can’t be modified. If a sample is made public, it is available for every user and group and for external visitors.",
  `id`  INT     NOT NULL AUTO_INCREMENT COMMENT "Sample unique internal identifier",
  `source_id`   INT     NOT NULL    COMMENT "To which part does the current element belong?",
  `created` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT "Date created",
  `updated` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT "Date updated",
  `user_id` INT     NOT NULL    COMMENT "User",
  `txnr`    INT     NULL DEFAULT NULL   COMMENT "NCBI Taxonomy number",
  `cult`    ENUM    ('cultured','uncultured')   NULL DEFAULT NULL   COMMENT "Is the sample cultured or uncultured?",
  `koma`    ENUM    ('METAGENOME', 'METATRANSCRIPTOME', 'METAVIROME', 'GENOME PROCARIOTA', 'GENOME VIRUS', 'PROTEOMICS', 'SINGLE CELL GENOMICS', 'PLASMID') NOT NULL    COMMENT "Kind of material",
  `meca`    VARCHAR (20)    NULL DEFAULT NULL   COMMENT "INSDC (International Nucleotide Sequence Database Collaboration) metagenome accession number.",
  `gsiz`    INT     NULL DEFAULT NULL   COMMENT "Estimated (for incomplete) or actual (for complete) genome/metagenome size. Unit bp (base pairs)",
  `dnae`    INT     NULL DEFAULT NULL   COMMENT "DNA extraction method",
  `seqt`    INT     NULL DEFAULT NULL   COMMENT "Sequencing Technology",
  `dati`    DATE        NULL DEFAULT NULL   COMMENT "Date of isolation",
  `sfrac`   INT     NULL DEFAULT NULL   COMMENT "Sequenced fraction",
  `rreads`  VARCHAR (40)    NULL DEFAULT NULL   COMMENT "Raw reads. An uuid unique identifier of the file into the server's filesystem.",
  `rreads2` VARCHAR (40)    NULL DEFAULT NULL   COMMENT "Raw reads, second file. An uuid unique identifier of the possible second file into the server's filesystem.",
  `rrname`  VARCHAR (100)   NULL DEFAULT NULL   COMMENT "Name of the original file containing the raw reads",
  `rrname2` VARCHAR (100)   NULL DEFAULT NULL   COMMENT "Name of the second original file containing the raw reads",
  `rreadacc`    INT     NULL DEFAULT NULL   COMMENT "Raw reads NCBI accesion code",
  `rreadsnum`   INT     NULL DEFAULT NULL   COMMENT "Number of raw reads.",
  `rreadsbp`    INT     NULL DEFAULT NULL   COMMENT "Number of base pairs of raw reads",
  PRIMARY KEY (`id`),
  INDEX `fk_experiment_sample_1_idx` (`source_id` ASC),
  CONSTRAINT `fk_experiment_sample_1`
    FOREIGN KEY (`source_id`)
    REFERENCES `halodb`.`sample` (`id`),
  INDEX `fk_experiment_user_1_idx` (`user_id` ASC),
  CONSTRAINT `fk_experiment_user_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  INDEX `fk_experiment_fraction_1_idx` (`sfrac` ASC),
  CONSTRAINT `fk_experiment_fraction_1`
    FOREIGN KEY (`sfrac`)
    REFERENCES `halodb`.`fraction` (`id`),
  INDEX `fk_experiment_extraction_1_idx` (`dnae` ASC),
  CONSTRAINT `fk_experiment_extraction_1`
    FOREIGN KEY (`dnae`)
    REFERENCES `halodb`.`extraction` (`id`),
  INDEX `fk_experiment_sequencing_1_idx` (`seqt` ASC),
  CONSTRAINT `fk_experiment_sequencing_1`
    FOREIGN KEY (`seqt`)
    REFERENCES `halodb`.`sequencing` (`id`)
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
