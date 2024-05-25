-- MySQL Script generated by MySQL Workbench
-- Sat May 25 12:56:13 2024
-- Model: General    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema halodb
-- -----------------------------------------------------
-- The HaloDB 
DROP SCHEMA IF EXISTS `halodb` ;

-- -----------------------------------------------------
-- Schema halodb
--
-- The HaloDB 
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `halodb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `halodb` ;

-- -----------------------------------------------------
-- Table `halodb`.`assembly`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`assembly` ;

CREATE TABLE IF NOT EXISTS `halodb`.`assembly` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(40) NOT NULL COMMENT 'Software used for assembly',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `uid` VARCHAR(40) NOT NULL COMMENT 'Firebase unique identifier',
  `name` VARCHAR(80) NOT NULL,
  `surname` VARCHAR(80) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL,
  `email` VARCHAR(256) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `registration_time` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uid_UNIQUE` (`uid` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`author`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`author` ;

CREATE TABLE IF NOT EXISTS `halodb`.`author` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `author` VARCHAR(80) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL,
  `user_id` INT NULL DEFAULT NULL,
  `email` VARCHAR(256) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_authors_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_author_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`binning`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`binning` ;

CREATE TABLE IF NOT EXISTS `halodb`.`binning` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(40) NOT NULL COMMENT 'Binning software used',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`project`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`project` ;

CREATE TABLE IF NOT EXISTS `halodb`.`project` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(80) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `description` VARCHAR(400) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`experiment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`experiment` ;

CREATE TABLE IF NOT EXISTS `halodb`.`experiment` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(80) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `description` VARCHAR(400) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL,
  `project_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_experiments_projects1_idx` (`project_id` ASC),
  CONSTRAINT `fk_experiment_project`
    FOREIGN KEY (`project_id`)
    REFERENCES `halodb`.`project` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`fraction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`fraction` ;

CREATE TABLE IF NOT EXISTS `halodb`.`fraction` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(40) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
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
  `description` VARCHAR(40) NOT NULL COMMENT 'DNA extraction method',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`group`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(80) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `description` VARCHAR(400) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL,
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
  `description` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`publication`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`publication` ;

CREATE TABLE IF NOT EXISTS `halodb`.`publication` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `titl` VARCHAR(400) NULL DEFAULT NULL COMMENT 'Title',
  `jour` VARCHAR(80) NULL DEFAULT NULL COMMENT 'Journal',
  `volume` VARCHAR(20) NULL DEFAULT NULL COMMENT 'Volume',
  `pages` VARCHAR(20) NULL DEFAULT NULL COMMENT 'Pages',
  `doi` VARCHAR(400) NULL DEFAULT NULL COMMENT 'Publication DOI',
  `sample_id` INT NOT NULL,
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
  `description` VARCHAR(40) NOT NULL COMMENT 'Sequencing Technology',
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
  `description` VARCHAR(40) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
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
-- Table `halodb`.`sample`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`sample` ;

CREATE TABLE IF NOT EXISTS `halodb`.`sample` (
  `is_public` TINYINT NULL DEFAULT 0 COMMENT 'True if the sample is public. That means it can’t be modified. If a sample is made public, it is available for every user and group and for external visitors.',
  `id` INT NOT NULL AUTO_INCREMENT COMMENT 'Sample unique internal identifier',
  `experiment_id` INT NULL DEFAULT NULL COMMENT 'The sample belongs to an experiment',
  `name` VARCHAR(100) NULL DEFAULT NULL COMMENT 'Sample name',
  `stype` VARCHAR(200) NULL DEFAULT NULL COMMENT 'Sample type. Description of the sample',
  `ssize` FLOAT(11) NULL DEFAULT NULL COMMENT 'Sample size (weight, volume)',
  `ssizeunit` ENUM('μl', 'ml', 'l', 'g', 'Kg') CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Units of ssize',
  `created` DATETIME NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Date created',
  `updated` DATETIME NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Date updated',
  `user_id` INT NOT NULL COMMENT 'User',
  `cult` ENUM('cultured', 'uncultured') CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Is the sample cultured or uncultured?',
  `koma` ENUM('isolate', 'MAG', 'SAG', 'virus', 'viral contig', 'plasmid') CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Kind of material',
  `typn` TINYINT(4) NULL DEFAULT NULL COMMENT 'Is this the designed type material for a new taxon?',
  `otyp` VARCHAR(30) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'If it is not a new taxon (TYPN = false), indicate the strain or MAG or SAG from which the reference taxon was obtained.',
  `txnr` INT(11) NULL DEFAULT NULL COMMENT 'NCBI Taxonomy number of the type material (in case of member of an extant taxon)',
  `ccsu` TINYINT(4) NULL DEFAULT NULL COMMENT 'If cultured, has been submitted to culture collection?',
  `type` VARCHAR(30) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Designated type strain name/MAG/SAG (if TYPN)',
  `coln` VARCHAR(80) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Strain collection numbers',
  `coth` VARCHAR(500) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Other',
  `publication` INT NULL DEFAULT NULL COMMENT 'Publication data',
  `sixteensr` VARCHAR(20) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT '16S rRNA gene accession number',
  `meca` VARCHAR(20) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'INSDC (International Nucleotide Sequence Database Collaboration) metagenome accession number.',
  `twentythreesr` VARCHAR(20) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT '23S rRNA gene accession number',
  `gare` VARCHAR(20) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'genome/MAG/SAG accession number [RefSeq/ENA]',
  `seqdepth` INT(11) NULL DEFAULT NULL COMMENT 'Sequencing depth (Isolates/MAG)',
  `binn` VARCHAR(20) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'genome/MAG/SAG accession number [other]',
  `gsta` ENUM('complete', 'partial', 'draft') CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Genome status',
  `completeness` FLOAT(11) NULL DEFAULT NULL COMMENT 'Completeness (0%-100%). Percentage of the genome already processed.',
  `contamination` FLOAT(11) NULL DEFAULT NULL COMMENT 'Level of contamination (0%-100%). Proportion of reads not belonging to MAGs detected. ',
  `method` INT(11) NULL DEFAULT NULL COMMENT 'Method used to estimate the integrity and contamination of the sample.',
  `gsiz` INT(11) NULL DEFAULT NULL COMMENT 'Estimated (for incomplete) or actual (for complete) genome/metagenome size. Unit bp (base pairs)',
  `ggcm` FLOAT(11) NULL DEFAULT NULL COMMENT 'Molar percentage of Guanine and Cytosine in DNA.',
  `dnae` INT NULL DEFAULT NULL COMMENT 'DNA extraction method',
  `asem` INT NULL DEFAULT NULL COMMENT 'Software used for assembly',
  `asftparams` VARCHAR(80) NULL DEFAULT NULL COMMENT 'Parameters used with asem',
  `seqt` INT NULL DEFAULT NULL COMMENT 'Sequencing Technology',
  `bins` INT NULL DEFAULT NULL COMMENT 'Binning software used',
  `binsparams` VARCHAR(80) NULL DEFAULT NULL COMMENT 'Params used with bins',
  `coun` VARCHAR(30) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Country of origin',
  `regi` VARCHAR(30) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Region of origin',
  `geol` VARCHAR(80) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Geographic location',
  `lati` FLOAT(11) NULL DEFAULT NULL COMMENT 'Latitude',
  `long` FLOAT(11) NULL DEFAULT NULL COMMENT 'Longitude',
  `alti` FLOAT(11) NULL DEFAULT NULL COMMENT 'Altitude in meters, over level at sea, where the sample was taken.',
  `dept` FLOAT(11) NULL DEFAULT NULL COMMENT 'Depth, in meters, where the sample was taken, with respect to the fild alti. That is, if the sample was taken in a lake placed on a mountain, alti contains the altitude of the lake\'s surface and dept represents the depth into the lake where the sample was taken.',
  `sour` VARCHAR(80) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Source of sample',
  `dats` DATE NULL DEFAULT NULL COMMENT 'Sampling date',
  `hocs` TIME NULL DEFAULT NULL COMMENT 'Hour of collection of the sample [sharp hours]',
  `dati` DATE NULL DEFAULT NULL COMMENT 'Date of isolation',
  `tems` FLOAT(11) NULL DEFAULT NULL COMMENT 'Temperature of the sample [in celsius degrees]',
  `phsa` FLOAT(11) NULL DEFAULT NULL COMMENT 'pH of the sample',
  `sals` FLOAT(11) NULL DEFAULT NULL COMMENT 'Salinity of the sample [in percentage %]',
  `emet` VARCHAR(500) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Energy metabolism',
  `orel` INT(11) NULL DEFAULT NULL COMMENT 'Relationship with O2',
  `elac` VARCHAR(40) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Terminal electron acceptor',
  `temo` FLOAT(11) NULL DEFAULT NULL COMMENT 'Temperature optimum',
  `teml` FLOAT(11) NULL DEFAULT NULL COMMENT 'Lowest temperature for growth',
  `temh` FLOAT(11) NULL DEFAULT NULL COMMENT 'Highest temperature for growth',
  `phop` FLOAT(11) NULL DEFAULT NULL COMMENT 'pH optimum',
  `phlo` FLOAT(11) NULL DEFAULT NULL COMMENT 'Lowest pH for growth',
  `phhi` FLOAT(11) NULL DEFAULT NULL COMMENT 'Highest pH for growth',
  `salo` FLOAT(11) NULL DEFAULT NULL COMMENT 'Salinity optimum (0%-100%)',
  `sall` FLOAT(11) NULL DEFAULT NULL COMMENT 'Lowest NaCl concentration for growth',
  `salh` FLOAT(11) NULL DEFAULT NULL COMMENT 'Highest NaCl concentration for growth',
  `salw` VARCHAR(80) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Other salts besides NaCl to be reported',
  `bios` ENUM('BSL-1', 'BSL-2', 'BSL-3', 'BSL-4') CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Biosafety level',
  `habt` VARCHAR(100) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Habitat. Description of place where the sample was collected.',
  `bior` VARCHAR(100) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Biotic relationship with other organisms.',
  `host` VARCHAR(100) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'If it is a symbiont, with which host does it interact?',
  `path` VARCHAR(200) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Known pathogenicity.',
  `extr` VARCHAR(500) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Miscellaneous, extraordinary features relevant for the description',
  `sfrac` INT(11) NULL DEFAULT NULL COMMENT 'Sequenced fraction',
  `target` INT(11) NULL DEFAULT NULL COMMENT 'Target nucleic acids',
  `rreads` VARCHAR(40) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Raw reads',
  `rreadacc` INT(11) NULL DEFAULT NULL COMMENT 'Raw reads NCBI accesion code',
  `rrname` VARCHAR(100) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Name of the original file containing the raw reads',
  `rreadsnum` INT(11) NULL DEFAULT NULL COMMENT 'Number of raw reads.',
  `rreadsbp` INT(11) NULL DEFAULT NULL COMMENT 'Number of base pairs of raw reads',
  `treads` VARCHAR(40) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Trimmed reads',
  `trname` VARCHAR(100) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Name of the original file containing the trimmed reads',
  `treadsnum` INT(11) NULL DEFAULT NULL COMMENT 'Number of trimmed reads',
  `treadsbp` INT(11) NULL DEFAULT NULL COMMENT 'Number of base pairs in trimmed reads.',
  `coverage` FLOAT(11) NULL DEFAULT NULL COMMENT 'Coverage (Nonpareil)',
  `assembled` VARCHAR(40) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Identificador del fitxer d’assembled',
  `assname` VARCHAR(100) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Name of the original file containing the assembly',
  `asize` INT(11) NULL DEFAULT NULL COMMENT 'Assembly size in base pairs',
  `contignumber` INT(11) NULL DEFAULT NULL COMMENT 'Number of contigs',
  `pgenes` VARCHAR(40) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Predicted genes',
  `pgenesname` VARCHAR(100) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Name of the original file containing the predicted genes',
  `nagoya` VARCHAR(500) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Information related to the Nagoya Protocol',
  `sequrl` VARCHAR(400) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT '¡Atención! No hay indicios, aclarar qué señala esta URL. ¿Puede ser lo mismo que sequrl?',
  `strccol` INT NULL DEFAULT NULL COMMENT 'Strain Collection number',
  PRIMARY KEY (`id`),
  INDEX `fk_samples_experiments1_idx` (`experiment_id` ASC),
  INDEX `fk_samples_users1_idx` (`user_id` ASC),
  INDEX `fk_samples_oxygen1_idx` (`orel` ASC),
  INDEX `fk_samples_fraction1_idx` (`sfrac` ASC),
  INDEX `fk_samples_target1_idx` (`target` ASC),
  INDEX `fk_sample_method1_idx` (`method` ASC),
  INDEX `fk_sample_publication1` (`publication` ASC),
  INDEX `fk_sample_assembly1_idx` (`asem` ASC),
  INDEX `fk_sample_extraction1_idx` (`dnae` ASC),
  INDEX `fk_sample_sequencing1_idx` (`seqt` ASC),
  INDEX `fk_sample_binning_idx` (`bins` ASC),
  CONSTRAINT `fk_sample_assembly1`
    FOREIGN KEY (`asem`)
    REFERENCES `halodb`.`assembly` (`id`),
  CONSTRAINT `fk_sample_binning1`
    FOREIGN KEY (`bins`)
    REFERENCES `halodb`.`binning` (`id`),
  CONSTRAINT `fk_sample_extraction1`
    FOREIGN KEY (`dnae`)
    REFERENCES `halodb`.`extraction` (`id`),
  CONSTRAINT `fk_sample_method1`
    FOREIGN KEY (`method`)
    REFERENCES `halodb`.`method` (`id`),
  CONSTRAINT `fk_sample_publication1`
    FOREIGN KEY (`publication`)
    REFERENCES `halodb`.`publication` (`id`),
  CONSTRAINT `fk_sample_sequencing1`
    FOREIGN KEY (`seqt`)
    REFERENCES `halodb`.`sequencing` (`id`),
  CONSTRAINT `fk_sample_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  CONSTRAINT `fk_samples_experiments1`
    FOREIGN KEY (`experiment_id`)
    REFERENCES `halodb`.`experiment` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_samples_fraction1`
    FOREIGN KEY (`sfrac`)
    REFERENCES `halodb`.`fraction` (`id`),
  CONSTRAINT `fk_samples_oxygen1`
    FOREIGN KEY (`orel`)
    REFERENCES `halodb`.`oxygen` (`id`),
  CONSTRAINT `fk_samples_target1`
    FOREIGN KEY (`target`)
    REFERENCES `halodb`.`target` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`group_sharing_sample`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group_sharing_sample` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group_sharing_sample` (
  `group_id` INT(11) NOT NULL,
  `sample_id` INT(11) NOT NULL,
  `access_mode` ENUM('read', 'readwrite') NULL DEFAULT NULL,
  PRIMARY KEY (`group_id`, `sample_id`),
  INDEX `fk_groups_has_samples_samples1_idx` (`sample_id` ASC),
  INDEX `fk_groups_has_samples_groups1_idx` (`group_id` ASC),
  CONSTRAINT `fk_groups_has_samples_groups1`
    FOREIGN KEY (`group_id`)
    REFERENCES `halodb`.`group` (`id`),
  CONSTRAINT `fk_groups_has_samples_samples1`
    FOREIGN KEY (`sample_id`)
    REFERENCES `halodb`.`sample` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`hkgenes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`hkgenes` ;

CREATE TABLE IF NOT EXISTS `halodb`.`hkgenes` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'Identification of a housekeeping gene',
  `gene` VARCHAR(25) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_bin' NULL DEFAULT NULL COMMENT 'table of generic genes. To be used as housekeeping genes.',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`housekeeping`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`housekeeping` ;

CREATE TABLE IF NOT EXISTS `halodb`.`housekeeping` (
  `hkgenes_id` INT(11) NOT NULL,
  `sample_id` INT(11) NOT NULL,
  PRIMARY KEY (`hkgenes_id`, `sample_id`),
  INDEX `fk_hkgenes_has_sample_sample1_idx` (`sample_id` ASC),
  INDEX `fk_hkgenes_has_sample_hkgenes1_idx` (`hkgenes_id` ASC),
  CONSTRAINT `fk_hkgenes_has_sample_hkgenes1`
    FOREIGN KEY (`hkgenes_id`)
    REFERENCES `halodb`.`hkgenes` (`id`),
  CONSTRAINT `fk_hkgenes_has_sample_sample1`
    FOREIGN KEY (`sample_id`)
    REFERENCES `halodb`.`sample` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`keywords`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`keywords` ;

CREATE TABLE IF NOT EXISTS `halodb`.`keywords` (
  `id` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `keyword` VARCHAR(50) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
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
-- Table `halodb`.`publication_has_author`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`publication_has_author` ;

CREATE TABLE IF NOT EXISTS `halodb`.`publication_has_author` (
  `author_id` INT(11) NOT NULL,
  `publication_id` INT(11) NOT NULL,
  `coau` TINYINT(4) NULL DEFAULT '0' COMMENT 'The author is a corresponding author of the publication.',
  PRIMARY KEY (`author_id`, `publication_id`),
  INDEX `fk_publication_has_author_samples1_idx` (`publication_id` ASC),
  INDEX `fk_publication_has_author_users1_idx` (`author_id` ASC),
  CONSTRAINT `fk_publication_has_author_author1`
    FOREIGN KEY (`author_id`)
    REFERENCES `halodb`.`author` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_publication_has_author_publication1`
    FOREIGN KEY (`publication_id`)
    REFERENCES `halodb`.`publication` (`id`)
    ON DELETE CASCADE)
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


-- -----------------------------------------------------
-- Table `halodb`.`user_experiment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_experiment` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_experiment` (
  `user_id` INT NOT NULL,
  `experiment_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `experiment_id`),
  INDEX `fk_users_has_experiments_experiments1_idx` (`experiment_id` ASC),
  INDEX `fk_users_has_experiments_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_experiment_experiment1`
    FOREIGN KEY (`experiment_id`)
    REFERENCES `halodb`.`experiment` (`id`),
  CONSTRAINT `fk_user_experiment_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`user_project`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_project` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_project` (
  `user_id` INT NOT NULL,
  `project_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `project_id`),
  INDEX `fk_users_has_projects_projects1_idx` (`project_id` ASC),
  INDEX `fk_users_has_projects_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_project_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  CONSTRAINT `fk_users_has_projects_projects1`
    FOREIGN KEY (`project_id`)
    REFERENCES `halodb`.`project` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`sample_has_keywords`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`sample_has_keywords` ;

CREATE TABLE IF NOT EXISTS `halodb`.`sample_has_keywords` (
  `sample_id` INT(11) NOT NULL,
  `keywords_id` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  PRIMARY KEY (`sample_id`, `keywords_id`),
  INDEX `fk_sample_has_keywords_keywords1_idx` (`keywords_id` ASC),
  INDEX `fk_sample_has_keywords_sample1_idx` (`sample_id` ASC),
  CONSTRAINT `fk_sample_has_keywords_keywords1`
    FOREIGN KEY (`keywords_id`)
    REFERENCES `halodb`.`keywords` (`id`),
  CONSTRAINT `fk_sample_has_keywords_sample1`
    FOREIGN KEY (`sample_id`)
    REFERENCES `halodb`.`sample` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`user_shared_sample`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_shared_sample` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_shared_sample` (
  `user_id` INT(11) NOT NULL,
  `sample_id` INT(11) NOT NULL,
  `access_mode` ENUM('read', 'readwrite') CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT 'read' COMMENT 'Describes the acces mode to the sample. \'owner\' is the propietary, can read and write and also delete the sample. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.',
  PRIMARY KEY (`user_id`, `sample_id`),
  INDEX `fk_users_has_samples_samples1_idx` (`sample_id` ASC),
  INDEX `fk_users_has_samples_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_shared_sample_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_users_has_samples_samples1`
    FOREIGN KEY (`sample_id`)
    REFERENCES `halodb`.`sample` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`user_has_group`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_has_group` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_has_group` (
  `user_id` INT NOT NULL,
  `group_id` INT NOT NULL,
  `relation` ENUM('owner', 'member', 'invited') CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL COMMENT 'Describes the relationship of the user with the group. It can be \'owner\' (the user who has created the group) \'member\' (the user can access to the data, the samples, shared to the group) \'invited\' (the owner has invited the user, who will be member if he accept the invitation)',
  `addition_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'The date when the user has been invited or has accepted the invitation',
  PRIMARY KEY (`user_id`, `group_id`),
  INDEX `fk_users_has_groups_groups1_idx` (`group_id` ASC),
  INDEX `fk_users_has_groups_users_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_has_group_group1`
    FOREIGN KEY (`group_id`)
    REFERENCES `halodb`.`group` (`id`),
  CONSTRAINT `fk_users_has_groups_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

USE `halodb` ;

-- -----------------------------------------------------
-- procedure get_samples_available
-- -----------------------------------------------------

USE `halodb`;
DROP procedure IF EXISTS `halodb`.`get_samples_available`;

DELIMITER $$
USE `halodb`$$
CREATE DEFINER=`halodb`@`%` PROCEDURE `get_samples_available`(IN userId INT)
BEGIN
WITH relations AS (
SELECT 
    sa.id,
    MAX(sa.public) AS public,
    MAX(sa.owned) AS owned,
    MAX(sa.shared_by_group) AS shared_by_group,
    MAX(sa.shared_by_others) AS shared_by_others,
    MAX(sa.access_mode) AS access_mode, -- This assumes 'readwrite' > 'read'
    MAX(sa.group_relation) AS group_relation,
    MAX(sa.group_id) AS group_id,
    MAX(sa.group_name) AS group_name
  FROM (
	SELECT
		True AS public,
		False AS owned,
        False AS shared_by_group,
        False AS shared_by_others,
       'read' AS access_mode,
		NULL AS group_relation,
		NULL AS group_id, 
		NULL AS group_name, 
		s.id
	FROM sample AS s
	WHERE is_public=True
UNION ALL
	SELECT
		False AS public,
		True AS owned,
        False AS shared_by_group,
        False AS shared_by_others, 
		CASE WHEN s.is_public THEN 'read' ELSE 'readwrite' END AS access_mode,
		NULL AS group_relation,
		NULL AS group_id,
		NULL AS group_name,
		s.id
	FROM sample AS s
	WHERE s.user_id = userId
UNION ALL
	SELECT
		False AS public,
		False AS owned,
        True AS shared_by_group,
        False AS shared_by_others,  
        CASE WHEN s.is_public THEN 'read' WHEN s.user_id = userId THEN 'readwrite' ELSE gs.access_mode END AS access_mode,
        ug.relation AS group_relation,
        g.id AS group_id,
        g.name AS group_name,
        s.id
        FROM `halodb`.`group` AS g 
			JOIN `halodb`.`user_has_group` AS ug ON g.id = ug.group_id 
			JOIN `halodb`.`group_sharing_sample` AS gs ON ug.group_id = gs.group_id
			JOIN `halodb`.`sample` AS s ON gs.sample_id = s.id
	WHERE ug.user_id = userId
UNION ALL
	SELECT
		False AS public,
		False AS owned,
        False AS shared_by_group,
        True AS shared_by_others,
        CASE WHEN s.is_public THEN 'read' WHEN s.user_id = userId THEN 'readwrite' ELSE uss.access_mode END AS access_mode,
        NULL AS group_relation, 
        NULL AS group_id, 
        NULL AS group_name, 
        s.id
		FROM sample s
			JOIN user_shared_sample uss ON s.id = uss.sample_id
	WHERE uss.user_id = userId
) AS sa GROUP BY sa.id
) SELECT
	relations.public,
	relations.owned,
	relations.shared_by_group,
	relations.shared_by_others,
	relations.access_mode,
	relations.group_relation,
	relations.group_id,
	relations.group_name,
    sample.*
    FROM relations
    JOIN sample ON sample.id = relations.id
    ORDER BY id;
END$$

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
