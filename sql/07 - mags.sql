
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

USE `halodb` ;

-- -----------------------------------------------------
-- Table `halodb`.`mags`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`mags` ;
CREATE TABLE IF NOT EXISTS `halodb`.`mags` (
  `is_public`   BOOLEAN     NULL DEFAULT false  COMMENT "True if the sample is public. That means it can’t be modified. If a sample is made public, it is available for every user and group and for external visitors.",
  `id`  INT     NOT NULL AUTO_INCREMENT COMMENT "Sample unique internal identifier",
  `source_id`   INT     NOT NULL    COMMENT "To which part does the current element belong?",
  `created` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT "Date created",
  `updated` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT "Date updated",
  `user_id` INT     NOT NULL    COMMENT "User",
  `typn`    BOOLEAN     NULL DEFAULT false  COMMENT "Is this the designed type material for a new taxon?",
  `otyp`    VARCHAR (30)    NULL DEFAULT NULL   COMMENT "If it is not a new taxon (TYPN = false), indicate the strain or MAG or SAG from which the reference taxon was obtained.",
  `type`    VARCHAR (30)    NULL DEFAULT NULL   COMMENT "Designated type strain name/MAG/SAG (if TYPN)",
  `sixteensr`   VARCHAR (20)    NULL DEFAULT NULL   COMMENT "16S rRNA gene accession number",
  `seqdepth`    FLOAT       NULL DEFAULT NULL   COMMENT "Sequencing depth (Isolates/MAG)",
  `twentythreesr`   VARCHAR (20)    NULL DEFAULT NULL   COMMENT "23S rRNA gene accession number",
  `hkgn`    INT     NULL DEFAULT NULL   COMMENT "Alternative housekeeping genes",
  `meca`    VARCHAR (20)    NULL DEFAULT NULL   COMMENT "INSDC (International Nucleotide Sequence Database Collaboration) metagenome accession number.",
  `gare`    VARCHAR (20)    NULL DEFAULT NULL   COMMENT "genome/MAG/SAG accession number [RefSeq/ENA]",
  `binn`    VARCHAR (20)    NULL DEFAULT NULL   COMMENT "genome/MAG/SAG accession number [other]",
  `gsta`    enum    ("complete", "partial", "draft")    NULL DEFAULT NULL   COMMENT "Genome status",
  `completeness`    FLOAT       NULL DEFAULT NULL   COMMENT "Completeness (0%-100%). Percentage of the genome already processed.",
  `contamination`   FLOAT       NULL DEFAULT NULL   COMMENT "Level of contamination (0%-100%). Proportion of reads not belonging to MAGs detected. ",
  `method_id`   INT     NULL DEFAULT NULL   COMMENT "Method used to estimate the integrity and contamination of the sample.",
  `gsiz`    INT     NULL DEFAULT NULL   COMMENT "Estimated (for incomplete) or actual (for complete) genome/metagenome size. Unit bp (base pairs)",
  `ggcm`    FLOAT       NULL DEFAULT NULL   COMMENT "Molar percentage of Guanine and Cytosine in DNA.",
  `asem`    INT     NULL DEFAULT NULL   COMMENT "Software used for assembly",
  `asftparams`  VARCHAR (80)    NULL DEFAULT NULL   COMMENT "Parameters used with asem",
  `bins`    INT     NULL DEFAULT NULL   COMMENT "Binning software used",
  `binsparams`  VARCHAR (80)    NULL DEFAULT NULL   COMMENT "Params used with bins",
  `bior`    VARCHAR (100)   NULL DEFAULT NULL   COMMENT "Biotic relationship with other organisms.",
  `host`    VARCHAR (100)   NULL DEFAULT NULL   COMMENT "If it is a symbiont, with which host does it interact?",
  `path`    VARCHAR (200)   NULL DEFAULT NULL   COMMENT "Known pathogenicity.",
  PRIMARY KEY (`id`),
  INDEX `fk_mags_predicted_genes_1_idx` (`source_id` ASC),
  CONSTRAINT `fk_mags_predicted_genes_1`
    FOREIGN KEY (`source_id`)
    REFERENCES `halodb`.`predicted_genes` (`id`),
  INDEX `fk_mags_user_1_idx` (`user_id` ASC),
  CONSTRAINT `fk_mags_user_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  INDEX `fk_mags_method_1_idx` (`method_id` ASC),
  CONSTRAINT `fk_mags_method_1`
    FOREIGN KEY (`method_id`)
    REFERENCES `halodb`.`method` (`id`),
  INDEX `fk_mags_assembly_1_idx` (`asem` ASC),
  CONSTRAINT `fk_mags_assembly_1`
    FOREIGN KEY (`id`)
    REFERENCES `halodb`.`assembly` (`id`),
  INDEX `fk_mags_binning_1_idx` (`bins` ASC),
  CONSTRAINT `fk_mags_binning_1`
    FOREIGN KEY (`bins`)
    REFERENCES `halodb`.`binning` (`id`)
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
