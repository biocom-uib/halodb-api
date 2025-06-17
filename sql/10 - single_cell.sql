
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

USE `halodb` ;

-- -----------------------------------------------------
-- Table `halodb`.`single_cell`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`single_cell` ;
CREATE TABLE IF NOT EXISTS `halodb`.`single_cell` (
  `is_public`   BOOLEAN     NULL DEFAULT false  COMMENT "True if the sample is public. That means it can’t be modified. If a sample is made public, it is available for every user and group and for external visitors.",
  `id`  INT     NOT NULL AUTO_INCREMENT COMMENT "Sample unique internal identifier",
  `source_id`   INT     NOT NULL    COMMENT "To which part does the current element belong?",
  `created` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT "Date created",
  `updated` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT "Date updated",
  `user_id` INT     NOT NULL    COMMENT "User",
  `typn`    BOOLEAN     NULL DEFAULT false  COMMENT "Is this the designed type material for a new taxon?",
  `otyp`    VARCHAR (30)    NULL DEFAULT NULL   COMMENT "If it is not a new taxon (TYPN = false), indicate the strain or MAG or SAG from which the reference taxon was obtained.",
  `txnt`    INT     NULL DEFAULT NULL   COMMENT "NCBI Taxonomy number of the type material (in case of member of an extant taxon)",
  `ccsu`    BOOLEAN     NULL DEFAULT false  COMMENT "If cultured, has been submitted to culture collection?",
  `type`    VARCHAR (30)    NULL DEFAULT NULL   COMMENT "Designated type strain name/MAG/SAG (if TYPN)",
  `coln`    VARCHAR (80)    NULL DEFAULT NULL   COMMENT "Strain collection numbers",
  `sixteensr`   VARCHAR (20)    NULL DEFAULT NULL   COMMENT "16S rRNA gene accession number",
  `seqdepth`    FLOAT       NULL DEFAULT NULL   COMMENT "Sequencing depth (Isolates/MAG)",
  `twentythreesr`   VARCHAR (20)    NULL DEFAULT NULL   COMMENT "23S rRNA gene accession number",
  `hkgn`    INT     NULL DEFAULT NULL   COMMENT "Alternative housekeeping genes",
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
  `bios`    ENUM    ("BSL-1","BSL-2","BSL-3","BSL-4")   NULL DEFAULT NULL   COMMENT "Biosafety level",
  `bior`    VARCHAR (100)   NULL DEFAULT NULL   COMMENT "Biotic relationship with other organisms.",
  `host`    VARCHAR (100)   NULL DEFAULT NULL   COMMENT "If it is a symbiont, with which host does it interact?",
  `path`    VARCHAR (200)   NULL DEFAULT NULL   COMMENT "Known pathogenicity.",
  `assembled`   VARCHAR (40)    NULL DEFAULT NULL   COMMENT "Identificador del fitxer d’assembled",
  `assname` VARCHAR (100)   NULL DEFAULT NULL   COMMENT "Name of the original file containing the assembly",
  `asize`   INT     NULL DEFAULT NULL   COMMENT "Assembly size in base pairs",
  `contignumber`    INT     NULL DEFAULT NULL   COMMENT "Number of contigs",
  PRIMARY KEY (`id`),
  INDEX `fk_single_cell_predicted_genes_1_idx` (`source_id` ASC),
  CONSTRAINT `fk_single_cell_predicted_genes_1`
    FOREIGN KEY (`source_id`)
    REFERENCES `halodb`.`predicted_genes` (`id`),
  INDEX `fk_single_cell_user_1_idx` (`user_id` ASC),
  CONSTRAINT `fk_single_cell_user_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  INDEX `fk_single_cell_method_1_idx` (`method_id` ASC),
  CONSTRAINT `fk_single_cell_method_1`
    FOREIGN KEY (`method_id`)
    REFERENCES `halodb`.`method` (`id`),
  INDEX `fk_single_cell_assembly_1_idx` (`asem` ASC),
  CONSTRAINT `fk_single_cell_assembly_1`
    FOREIGN KEY (`asem`)
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
