-- MySQL Script generated by MySQL Workbench
-- Wed May  8 00:03:33 2024
-- Model: New Model    Version: 1.0
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
CREATE SCHEMA IF NOT EXISTS `halodb` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;
USE `halodb` ;

-- -----------------------------------------------------
-- Table `halodb`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `uid` VARCHAR(40) NOT NULL COMMENT 'Firebase unique identifier',
  `name` VARCHAR(80) NOT NULL,
  `surname` VARCHAR(80) COLLATE 'utf8mb3_bin' NULL,
  `email` VARCHAR(256) COLLATE 'utf8mb3_bin' NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `registration_time` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uid_UNIQUE` (`uid` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`group`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(80) COLLATE 'utf8mb3_bin' NOT NULL,
  `description` VARCHAR(400) COLLATE 'utf8mb3_bin' NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`user_has_group`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_has_group` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_has_group` (
  `user_id` INT NOT NULL,
  `group_id` INT NOT NULL,
  `relation` ENUM('owner', 'member', 'invited') NULL COMMENT 'Describes the relationship of the user with the group. It can be \'owner\' (the user who has created the group) \'member\' (the user can access to the data, the samples, shared to the group) \'invited\' (the owner has invited the user, who will be member if he accept the invitation)',
  `addition_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'The date when the user has been invited or has accepted the invitation',
  PRIMARY KEY (`user_id`, `group_id`),
  INDEX `fk_users_has_groups_groups1_idx` (`group_id` ASC),
  INDEX `fk_users_has_groups_users_idx` (`user_id` ASC),
  CONSTRAINT `fk_users_has_groups_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  CONSTRAINT `fk_user_has_group_group1`
    FOREIGN KEY (`group_id`)
    REFERENCES `halodb`.`group` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`project`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`project` ;

CREATE TABLE IF NOT EXISTS `halodb`.`project` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(80) COLLATE 'utf8mb3_bin' NOT NULL,
  `description` VARCHAR(400) COLLATE 'utf8mb3_bin' NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`experiment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`experiment` ;

CREATE TABLE IF NOT EXISTS `halodb`.`experiment` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(80) COLLATE 'utf8mb3_bin' NOT NULL,
  `description` VARCHAR(400) COLLATE 'utf8mb3_bin' NULL,
  `project_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_experiments_projects1_idx` (`project_id` ASC),
  CONSTRAINT `fk_experiment_project`
    FOREIGN KEY (`project_id`)
    REFERENCES `halodb`.`project` (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`fraction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`fraction` ;

CREATE TABLE IF NOT EXISTS `halodb`.`fraction` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(40) COLLATE 'utf8mb3_bin' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`oxygen`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`oxygen` ;

CREATE TABLE IF NOT EXISTS `halodb`.`oxygen` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `relationship` VARCHAR(40) COLLATE 'utf8mb3_bin' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`ph`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`ph` ;

CREATE TABLE IF NOT EXISTS `halodb`.`ph` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(40) COLLATE 'utf8mb3_bin' NOT NULL,
  `vmin` FLOAT NULL,
  `vmax` FLOAT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`salinity`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`salinity` ;

CREATE TABLE IF NOT EXISTS `halodb`.`salinity` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(40) COLLATE 'utf8mb3_bin' NOT NULL,
  `vmin` FLOAT NULL,
  `vmax` FLOAT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`target`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`target` ;

CREATE TABLE IF NOT EXISTS `halodb`.`target` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) COLLATE 'utf8mb3_bin' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`temperature`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`temperature` ;

CREATE TABLE IF NOT EXISTS `halodb`.`temperature` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(40) COLLATE 'utf8mb3_bin' NOT NULL,
  `vmin` FLOAT NULL,
  `vmax` FLOAT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`method`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`method` ;

CREATE TABLE IF NOT EXISTS `halodb`.`method` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`sample`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`sample` ;

CREATE TABLE IF NOT EXISTS `halodb`.`sample` (
  `experiment_id` INT NULL DEFAULT NULL,
  `id` INT NOT NULL AUTO_INCREMENT COMMENT 'Sample unique internal identifier',
  `created` DATE NULL DEFAULT NULL COMMENT 'Date created',
  `updated` DATE NULL DEFAULT NULL COMMENT 'Date updated',
  `user_id` INT NULL DEFAULT NULL COMMENT 'User unique identifier, it\'s a link to the user table',
  `txnr` INT(11) NULL DEFAULT NULL COMMENT 'Taxonomic number',
  `version` VARCHAR(20) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Version. NCBI accession & version',
  `entrydate` DATE NULL DEFAULT NULL COMMENT 'Date of the entry',
  `firstdate` DATE NULL DEFAULT NULL COMMENT 'First submission date',
  `draftnumber` VARCHAR(8) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Draft number / date',
  `cult` ENUM('cultured', 'uncultured') CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Is the sample cultured or uncultured?',
  `koma` ENUM('isolate', 'MAG', 'SAG', 'virus', 'viral contig', 'plasmid') CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Kind of material',
  `typn` TINYINT(1) NULL DEFAULT NULL COMMENT 'Is this the designed type material for a new taxon? A true (1) or false (0) value',
  `otyp` VARCHAR(30) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Type strain/MAG/SAG (in case of member of an extant taxon)',
  `txnt` INT(11) NULL DEFAULT NULL COMMENT 'Taxonumber of the type material (in case of member of an extant taxon)',
  `ccsu` TINYINT(1) NULL DEFAULT NULL COMMENT 'If cultured, has been submitted to culture collection?  A true (1) or false (0) value',
  `type` VARCHAR(30) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Designated type strain name/MAG/SAG (if TYPN is true)',
  `coln` VARCHAR(80) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Strain collection numbers',
  `domain` VARCHAR(25) NULL DEFAULT NULL COMMENT 'Domain name',
  `kingdom` VARCHAR(25) NULL COMMENT 'Kingdom name',
  `phylum` VARCHAR(50) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Phylum name',
  `phylumety` VARCHAR(256) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Phylum etymology',
  `class` VARCHAR(50) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Class name',
  `classety` VARCHAR(256) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Class etymology',
  `order` VARCHAR(50) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Order  name',
  `orderety` VARCHAR(256) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Order etymology',
  `family` VARCHAR(50) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Family name',
  `familyety` VARCHAR(256) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Family etymology',
  `gena` VARCHAR(50) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Genus name',
  `gety` VARCHAR(256) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Genus etymology',
  `gent` VARCHAR(50) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Type species of the genus',
  `spep` VARCHAR(50) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Specific epithet of the species',
  `spty` VARCHAR(256) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Species etymology',
  `spna` VARCHAR(50) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Species name',
  `baso` VARCHAR(50) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Basonym',
  `ssna` VARCHAR(50) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Subspecies name',
  `ssty` VARCHAR(50) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Subspecies etymology',
  `coth` VARCHAR(500) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Other comments',
  `titl` VARCHAR(400) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Title',
  `jour` VARCHAR(80) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Journal',
  `volume` VARCHAR(20) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Volume',
  `pages` VARCHAR(20) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Pages',
  `doi` VARCHAR(400) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Publication DOI',
  `coau` VARCHAR(80) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Corresponding autor',
  `emau` VARCHAR(256) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'e-mail of the corresponding autor',
  `sixteensr` VARCHAR(20) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT '16S rRNA gene accession number',
  `hkgn` VARCHAR(20) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Alternative housekeeping genes',
  `meca` VARCHAR(20) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Metagenome accession number',
  `gare` VARCHAR(20) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'genome/MAG/SAG accession number [RefSeq/EMBL]',
  `gaem` VARCHAR(20) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'genome/MAG/SAG accession number [EMBL]',
  `binn` VARCHAR(20) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'genome/MAG/SAG accession number [other]',
  `url` VARCHAR(400) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'URL',
  `gsta` ENUM('complete', 'partial', 'draft') CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Genome status',
  `completeness` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'Completeness percentage',
  `contamination` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'Level of contamination percentage',
  `method` INT(11) NULL DEFAULT NULL COMMENT 'Method used to estimate completeness and contamination',
  `gsiz` INT(11) NULL DEFAULT NULL COMMENT 'Estimated (for incomplete) or actual (for complete) genome or metagenome size. Unit bp (base pairs)',
  `ggcm` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'GC mol %',
  `dnae` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'DNA extraction method',
  `asem` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Assembly method',
  `seqt` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Sequencing Technology',
  `bins` VARCHAR(80) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Binning software used and paràmetres',
  `asft` VARCHAR(80) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Assembly software used and paràmetres',
  `coun` VARCHAR(30) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Country of origin',
  `regi` VARCHAR(30) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Region of origin',
  `geol` VARCHAR(80) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Geographic location',
  `lati` FLOAT(11) NULL DEFAULT NULL COMMENT 'Latitude',
  `long` FLOAT(11) NULL DEFAULT NULL COMMENT 'Longitude',
  `alti` FLOAT(11) NULL DEFAULT NULL COMMENT 'Altitude in meters, over level at sea, where the sample was taken.',
  `dept` FLOAT(11) NULL DEFAULT NULL COMMENT 'Depth, in meters, where the sample was taken, with respect to the fild alti. That is, if the sample was taken in a lake placed on a mountain, alti contains the altitude of the lake\'s surface and dept represents the depth into the lake where the sample was taken.',
  `sour` VARCHAR(80) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Source of sample',
  `dats` DATE NULL DEFAULT NULL COMMENT 'Sampling date',
  `hocs` TIME NULL DEFAULT NULL COMMENT 'Hour of collection of the sample [sharp hours]',
  `dati` DATE NULL DEFAULT NULL COMMENT 'Date of isolation',
  `datu` DATE NULL DEFAULT NULL COMMENT 'Date of isolation if unknown',
  `tems` FLOAT(11) NULL DEFAULT NULL COMMENT 'Temperature of the sample [in celsius degrees]',
  `phsa` FLOAT(11) NULL DEFAULT NULL COMMENT 'pH of the sample',
  `sals` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'Salinity of the sample [in percentage %]',
  `emet` VARCHAR(500) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Energy metabolism',
  `orel` INT(11) NULL DEFAULT NULL COMMENT 'Relationship to O2. It\'s a foreign key for oxygen table',
  `elac` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Terminal electron acceptor',
  `temo` FLOAT(11) NULL DEFAULT NULL COMMENT 'Temperature optimum',
  `teml` FLOAT(11) NULL DEFAULT NULL COMMENT 'Lowest temperature for growth',
  `temh` FLOAT(11) NULL DEFAULT NULL COMMENT 'Highest temperature for growth',
  `temc` INT(11) NULL DEFAULT NULL COMMENT 'Temperature category. It\'s a foreign key for temperature table',
  `phop` FLOAT(11) NULL DEFAULT NULL COMMENT 'pH optimum',
  `phlo` FLOAT(11) NULL DEFAULT NULL COMMENT 'Lowest pH for growth',
  `phhi` FLOAT(11) NULL DEFAULT NULL COMMENT 'Highest pH for growth',
  `phca` INT(11) NULL DEFAULT NULL COMMENT 'pH category. It\'s a foreign key for ph table',
  `salo` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'Salinity optimum percentage',
  `sall` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'Lowest NaCl concentration percentage for growth',
  `salh` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'Highest NaCl concentration percentage for growth',
  `salw` VARCHAR(80) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Other salts besides NaCl to be reported',
  `salc` INT(11) NULL DEFAULT NULL COMMENT 'Salinity category. It\'s a foreign key for salinity table',
  `bios` ENUM('BSL-1', 'BSL-2', 'BSL-3', 'BSL-4') CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Biosafety level',
  `habt` VARCHAR(100) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Habitat of the sample',
  `bior` VARCHAR(100) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Biotic relationship',
  `host` VARCHAR(100) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Symbiosis with the host',
  `path` VARCHAR(200) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Known pathogenicity',
  `extr` VARCHAR(500) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Miscellaneous, extraordinary features relevant for the description',
  `name` VARCHAR(100) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Sample name',
  `stype` VARCHAR(200) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Sample type',
  `ssize` FLOAT(11) NULL DEFAULT NULL COMMENT 'Sample size',
  `ssizeunit` ENUM('μl', 'ml', 'l', 'g', 'Kg') CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Sample size units',
  `sfrac` INT(11) NULL DEFAULT NULL COMMENT 'Sequenced fraction. It\'s a foreign key for fraction table',
  `target` INT(11) NULL DEFAULT NULL COMMENT 'Target nucleic acids. It\'s a foreign key for target table',
  `rreads` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Raw reads. An uuid unique identifier of the file into the server\'s filesystem.',
  `rreadacc` INT(11) NULL DEFAULT NULL COMMENT 'Raw reads NCBI accesion code',
  `rrname` VARCHAR(100) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Name of the original file containing the raw reads',
  `rreadsnum` INT(11) NULL DEFAULT NULL COMMENT 'Amount of raw reads. Unit: bp (base pairs)',
  `treads` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Trimmed reads. An uuid unique identifier of the file into the server\'s filesystem.',
  `trname` VARCHAR(100) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Name of the original file containing the trimmed reads',
  `treadsnum` INT(11) NULL DEFAULT NULL COMMENT 'Amount of trimmed reads. Unit: bp (base pairs)',
  `coverage` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'Coverage percentage (Nonpareil)',
  `assembled` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Assembly file. An uuid unique identifier of the file into the server\'s filesystem.',
  `assname` VARCHAR(100) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Name of the original file containing the assembly',
  `asize` INT(11) NULL DEFAULT NULL COMMENT 'Assembly size. Unit: bp (base pairs)',
  `contignumber` INT(11) NULL DEFAULT NULL COMMENT 'Number of contigs',
  `pgenes` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Predicted genes. An uuid unique identifier of the file into the server\'s filesystem.',
  `pgenesname` VARCHAR(100) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Name of the original file containing the predicted names',
  `seqdepth` FLOAT(11) NULL DEFAULT NULL COMMENT 'Sequencing depth (Isolates/MAG)',
  `twentythreesr` VARCHAR(20) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT '23S rRNA gene accession number',
  `nagoya` VARCHAR(500) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Information related to the Nagoya Protocol',
  `sequrl` VARCHAR(400) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL COMMENT 'Sequence URL',
  PRIMARY KEY (`id`),
  INDEX `fk_samples_experiments1_idx` (`experiment_id` ASC),
  INDEX `fk_samples_users1_idx` (`user_id` ASC),
  INDEX `fk_samples_oxygen1_idx` (`orel` ASC),
  INDEX `fk_samples_temperature1_idx` (`temc` ASC),
  INDEX `fk_samples_ph1_idx` (`phca` ASC),
  INDEX `fk_samples_salinity1_idx` (`salc` ASC),
  INDEX `fk_samples_fraction1_idx` (`sfrac` ASC),
  INDEX `fk_samples_target1_idx` (`target` ASC),
  INDEX `fk_sample_method1_idx` (`method` ASC),
  CONSTRAINT `fk_samples_experiments1`
    FOREIGN KEY (`experiment_id`)
    REFERENCES `halodb`.`experiment` (`id`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_samples_fraction1`
    FOREIGN KEY (`sfrac`)
    REFERENCES `halodb`.`fraction` (`id`),
  CONSTRAINT `fk_samples_oxygen1`
    FOREIGN KEY (`orel`)
    REFERENCES `halodb`.`oxygen` (`id`),
  CONSTRAINT `fk_samples_ph1`
    FOREIGN KEY (`phca`)
    REFERENCES `halodb`.`ph` (`id`),
  CONSTRAINT `fk_samples_salinity1`
    FOREIGN KEY (`salc`)
    REFERENCES `halodb`.`salinity` (`id`),
  CONSTRAINT `fk_samples_target1`
    FOREIGN KEY (`target`)
    REFERENCES `halodb`.`target` (`id`),
  CONSTRAINT `fk_samples_temperature1`
    FOREIGN KEY (`temc`)
    REFERENCES `halodb`.`temperature` (`id`),
  CONSTRAINT `fk_sample_method1`
    FOREIGN KEY (`method`)
    REFERENCES `halodb`.`method` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_sample_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`user_shared_sample`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_shared_sample` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_shared_sample` (
  `user_id` INT NOT NULL,
  `sample_id` INT NOT NULL,
  `relation` ENUM('owner', 'read', 'readwrite') NULL DEFAULT 'read' COMMENT 'Describes the acces mode to the sample. \'owner\' is the propietary, can read and write and also delete the sample. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.',
  PRIMARY KEY (`user_id`, `sample_id`),
  INDEX `fk_users_has_samples_samples1_idx` (`sample_id` ASC),
  INDEX `fk_users_has_samples_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_users_has_samples_samples1`
    FOREIGN KEY (`sample_id`)
    REFERENCES `halodb`.`sample` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_shared_sample_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`group_sharing_sample`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group_sharing_sample` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group_sharing_sample` (
  `group_id` INT NOT NULL,
  `sample_id` INT NOT NULL,
  `read_only` TINYINT NULL DEFAULT 1 COMMENT 'If false, the sample can be modified by any member of the group. If true, the sample can only be read.',
  PRIMARY KEY (`group_id`, `sample_id`),
  INDEX `fk_groups_has_samples_samples1_idx` (`sample_id` ASC),
  INDEX `fk_groups_has_samples_groups1_idx` (`group_id` ASC),
  CONSTRAINT `fk_groups_has_samples_groups1`
    FOREIGN KEY (`group_id`)
    REFERENCES `halodb`.`group` (`id`),
  CONSTRAINT `fk_groups_has_samples_samples1`
    FOREIGN KEY (`sample_id`)
    REFERENCES `halodb`.`sample` (`id`))
ENGINE = InnoDB;


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
    REFERENCES `halodb`.`experiment` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_experiment_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


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
  CONSTRAINT `fk_users_has_projects_projects1`
    FOREIGN KEY (`project_id`)
    REFERENCES `halodb`.`project` (`id`),
  CONSTRAINT `fk_user_project_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`author`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`author` ;

CREATE TABLE IF NOT EXISTS `halodb`.`author` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `author` VARCHAR(80) COLLATE 'utf8mb3_bin' NULL,
  `sample_id` INT NOT NULL,
  `user_id` INT NULL,
  `corresponding_author` TINYINT NULL,
  `email` VARCHAR(256) COLLATE 'utf8mb3_bin' NULL,
  PRIMARY KEY (`id`, `sample_id`),
  INDEX `fk_authors_sample1_idx` (`sample_id` ASC),
  INDEX `fk_authors_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_authors_sample1`
    FOREIGN KEY (`sample_id`)
    REFERENCES `halodb`.`sample` (`id`),
  CONSTRAINT `fk_author_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`keywords`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`keywords` ;

CREATE TABLE IF NOT EXISTS `halodb`.`keywords` (
  `id` VARCHAR(45) COLLATE 'utf8mb3_bin' NOT NULL,
  `keyword` VARCHAR(50) COLLATE 'utf8mb3_bin' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`sample_has_keywords`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`sample_has_keywords` ;

CREATE TABLE IF NOT EXISTS `halodb`.`sample_has_keywords` (
  `sample_id` INT NOT NULL,
  `keywords_id` VARCHAR(45) COLLATE 'utf8mb3_bin' NOT NULL,
  PRIMARY KEY (`sample_id`, `keywords_id`),
  INDEX `fk_sample_has_keywords_keywords1_idx` (`keywords_id` ASC),
  INDEX `fk_sample_has_keywords_sample1_idx` (`sample_id` ASC),
  CONSTRAINT `fk_sample_has_keywords_keywords1`
    FOREIGN KEY (`keywords_id`)
    REFERENCES `halodb`.`keywords` (`id`),
  CONSTRAINT `fk_sample_has_keywords_sample1`
    FOREIGN KEY (`sample_id`)
    REFERENCES `halodb`.`sample` (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
