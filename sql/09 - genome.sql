
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

USE `halodb` ;

-- -----------------------------------------------------
-- Table `halodb`.`genome`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`genome` ;
CREATE TABLE IF NOT EXISTS `halodb`.`genome` (
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
  `dnae`    INT     NULL DEFAULT NULL   COMMENT "DNA extraction method",
  `asem`    INT     NULL DEFAULT NULL   COMMENT "Software used for assembly",
  `asftparams`  VARCHAR (80)    NULL DEFAULT NULL   COMMENT "Parameters used with asem",
  `seqt`    INT     NULL DEFAULT NULL   COMMENT "Sequencing Technology",
  `dati`    DATE        NULL DEFAULT NULL   COMMENT "Date of isolation",
  `tems`    FLOAT       NULL DEFAULT NULL   COMMENT "Temperature of the sample [in celsius degrees]",
  `phsa`    FLOAT       NULL DEFAULT NULL   COMMENT "pH of the sample",
  `sals`    FLOAT       NULL DEFAULT NULL   COMMENT "Salinity of the sample [in percentage %]",
  `emet`    VARCHAR (500)   NULL DEFAULT NULL   COMMENT "Energy metabolism",
  `orel`    INT     NULL DEFAULT NULL   COMMENT "Relationship with O2",
  `elac`    VARCHAR (40)        COMMENT "Terminal electron acceptor",
  `temo`    FLOAT           COMMENT "Temperature optimum",
  `teml`    FLOAT           COMMENT "Lowest temperature for growth",
  `temh`    FLOAT           COMMENT "Highest temperature for growth",
  `phop`    FLOAT       NULL DEFAULT NULL   COMMENT "pH optimum",
  `phlo`    FLOAT       NULL DEFAULT NULL   COMMENT "Lowest pH for growth",
  `phhi`    FLOAT       NULL DEFAULT NULL   COMMENT "Highest pH for growth",
  `salo`    FLOAT       NULL DEFAULT NULL   COMMENT "Salinity optimum (0%-100%)",
  `sall`    FLOAT       NULL DEFAULT NULL   COMMENT "Lowest NaCl concentration for growth",
  `salh`    FLOAT       NULL DEFAULT NULL   COMMENT "Highest NaCl concentration for growth",
  `salw`    VARCHAR (80)    NULL DEFAULT NULL   COMMENT "Other salts besides NaCl to be reported",
  `bios`    ENUM    ("BSL-1","BSL-2","BSL-3","BSL-4")   NULL DEFAULT NULL   COMMENT "Biosafety level",
  `bior`    VARCHAR (100)   NULL DEFAULT NULL   COMMENT "Biotic relationship with other organisms.",
  `host`    VARCHAR (100)   NULL DEFAULT NULL   COMMENT "If it is a symbiont, with which host does it interact?",
  `path`    VARCHAR (200)   NULL DEFAULT NULL   COMMENT "Known pathogenicity.",
  `extr`    VARCHAR (500)   NULL DEFAULT NULL   COMMENT "Miscellaneous, extraordinary features relevant for the description",
  `assembled`   VARCHAR (40)    NULL DEFAULT NULL   COMMENT "Identificador del fitxer d’assembled",
  `assname` VARCHAR (100)   NULL DEFAULT NULL   COMMENT "Name of the original file containing the assembly",
  `asize`   INT     NULL DEFAULT NULL   COMMENT "Assembly size in base pairs",
  `contignumber`    INT     NULL DEFAULT NULL   COMMENT "Number of contigs",
  `strccol` INT     NULL DEFAULT NULL   COMMENT "Strain Collection number",
  PRIMARY KEY (`id`),
  INDEX `fk_genome_predicted_genes_1_idx` (`source_id` ASC),
  CONSTRAINT `fk_genome_predicted_genes_1`
    FOREIGN KEY (`source_id`)
    REFERENCES `halodb`.`predicted_genes` (`id`),
  INDEX `fk_genome_user_1_idx` (`user_id` ASC),
  CONSTRAINT `fk_genome_user_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  INDEX `fk_genome_oxygen_1_idx` (`orel` ASC),
  CONSTRAINT `fk_genome_oxygen_1`
    FOREIGN KEY (`orel`)
    REFERENCES `halodb`.`oxygen` (`id`),
  INDEX `fk_genome_method_1_idx` (`method_id` ASC),
  CONSTRAINT `fk_genome_method_1`
    FOREIGN KEY (`method_id`)
    REFERENCES `halodb`.`method` (`id`),
  INDEX `fk_genome_assembly_1_idx` (`asem` ASC),
  CONSTRAINT `fk_genome_assembly_1`
    FOREIGN KEY (`id`)
    REFERENCES `halodb`.`assembly` (`id`),
  INDEX `fk_genome_extraction_1_idx` (`dnae` ASC),
  CONSTRAINT `fk_genome_extraction_1`
    FOREIGN KEY (`dnae`)
    REFERENCES `halodb`.`extraction` (`id`),
  INDEX `fk_genome_sequencing_1_idx` (`seqt` ASC),
  CONSTRAINT `fk_genome_sequencing_1`
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
