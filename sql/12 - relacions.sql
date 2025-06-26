
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

USE `halodb` ;

-- -----------------------------------------------------
-- Table `halodb`.`user_shared_sample`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_shared_sample` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_shared_sample` (
  `user_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'owner\' is the propietary, can read and write and also delete the sample. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`user_id`, `shared_id`),
  INDEX `fk_user_has_sample_1_INTx` (`shared_id` ASC),
  INDEX `fk_user_has_sample_1_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_shared_sample_1_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  CONSTRAINT `fk_user_shared_sample_1_sample`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`sample` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`group_shared_sample`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group_shared_sample` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group_shared_sample` (
  `group_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'group\' is the group with some kind of access. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`group_id`, `shared_id`),
  INDEX `fk_group_shared_sample_1_INTx` (`shared_id` ASC),
  INDEX `fk_group_shared_sample_1_group_idx` (`group_id` ASC),
  CONSTRAINT `fk_group_shared_sample_1_group`
    FOREIGN KEY (`group_id`)
    REFERENCES `halodb`.`group` (`id`),
  CONSTRAINT `fk_group_shared_sample_1_sample`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`sample` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`user_shared_experiment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_shared_experiment` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_shared_experiment` (
  `user_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'owner\' is the propietary, can read and write and also delete the sample. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`user_id`, `shared_id`),
  INDEX `fk_user_has_experiment_1_experiment_idx` (`shared_id` ASC),
  INDEX `fk_user_has_experiment_1_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_shared_experiment_1_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  CONSTRAINT `fk_user_shared_experiment_1_experiment`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`experiment` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`group_shared_experiment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group_shared_experiment` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group_shared_experiment` (
  `group_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'group\' is the group with some kind of access. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`group_id`, `shared_id`),
  INDEX `fk_group_shared_experiment_1_experiment_idx` (`shared_id` ASC),
  INDEX `fk_group_shared_experiment_1_group_idx` (`group_id` ASC),
  CONSTRAINT `fk_group_shared_experiment_1_group`
    FOREIGN KEY (`group_id`)
    REFERENCES `halodb`.`group` (`id`),
  CONSTRAINT `fk_group_shared_experiment_1_experiment`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`experiment` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`user_shared_trimmed_reads`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_shared_trimmed_reads` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_shared_trimmed_reads` (
  `user_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'owner\' is the propietary, can read and write and also delete the sample. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`user_id`, `shared_id`),
  INDEX `fk_user_has_trimmed_reads_1_trimmed_reads_idx` (`shared_id` ASC),
  INDEX `fk_user_has_trimmed_reads_1_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_shared_trimmed_reads_1_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  CONSTRAINT `fk_user_shared_trimmed_reads_1_trimmed_reads`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`trimmed_reads` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`group_shared_trimmed_reads`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group_shared_trimmed_reads` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group_shared_trimmed_reads` (
  `group_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'group\' is the group with some kind of access. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`group_id`, `shared_id`),
  INDEX `fk_group_shared_trimmed_reads_1_trimmed_reads_idx` (`shared_id` ASC),
  INDEX `fk_group_shared_trimmed_reads_1_group_idx` (`group_id` ASC),
  CONSTRAINT `fk_group_shared_trimmed_reads_1_group`
    FOREIGN KEY (`group_id`)
    REFERENCES `halodb`.`group` (`id`),
  CONSTRAINT `fk_group_shared_trimmed_reads_1_trimmed_reads`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`trimmed_reads` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`user_shared_contigs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_shared_contigs` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_shared_contigs` (
  `user_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'owner\' is the propietary, can read and write and also delete the sample. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`user_id`, `shared_id`),
  INDEX `fk_user_has_contigs_1_contigs_idx` (`shared_id` ASC),
  INDEX `fk_user_has_contigs_1_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_shared_contigs_1_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  CONSTRAINT `fk_user_shared_contigs_1_contigs`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`contigs` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`group_shared_contigs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group_shared_contigs` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group_shared_contigs` (
  `group_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'group\' is the group with some kind of access. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`group_id`, `shared_id`),
  INDEX `fk_group_shared_contigs_1_contigs_idx` (`shared_id` ASC),
  INDEX `fk_group_shared_contigs_1_group_idx` (`group_id` ASC),
  CONSTRAINT `fk_group_shared_contigs_1_group`
    FOREIGN KEY (`group_id`)
    REFERENCES `halodb`.`group` (`id`),
  CONSTRAINT `fk_group_shared_contigs_1_contigs`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`contigs` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`user_shared_predicted_genes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_shared_predicted_genes` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_shared_predicted_genes` (
  `user_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'owner\' is the propietary, can read and write and also delete the sample. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`user_id`, `shared_id`),
  INDEX `fk_user_has_predicted_genes_1_predicted_genes_idx` (`shared_id` ASC),
  INDEX `fk_user_has_predicted_genes_1_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_shared_predicted_genes_1_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  CONSTRAINT `fk_user_shared_predicted_genes_1_predicted_genes`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`predicted_genes` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`group_shared_predicted_genes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group_shared_predicted_genes` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group_shared_predicted_genes` (
  `group_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'group\' is the group with some kind of access. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`group_id`, `shared_id`),
  INDEX `fk_group_shared_predicted_genes_1_predicted_genes_idx` (`shared_id` ASC),
  INDEX `fk_group_shared_predicted_genes_1_group_idx` (`group_id` ASC),
  CONSTRAINT `fk_group_shared_predicted_genes_1_group`
    FOREIGN KEY (`group_id`)
    REFERENCES `halodb`.`group` (`id`),
  CONSTRAINT `fk_group_shared_predicted_genes_1_predicted_genes`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`predicted_genes` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`user_shared_mags`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_shared_mags` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_shared_mags` (
  `user_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'owner\' is the propietary, can read and write and also delete the sample. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`user_id`, `shared_id`),
  INDEX `fk_user_has_mags_1_mags_idx` (`shared_id` ASC),
  INDEX `fk_user_has_mags_1_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_shared_mags_1_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  CONSTRAINT `fk_user_shared_mags_1_mags`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`mags` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`group_shared_mags`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group_shared_mags` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group_shared_mags` (
  `group_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'group\' is the group with some kind of access. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`group_id`, `shared_id`),
  INDEX `fk_group_shared_mags_1_mags_idx` (`shared_id` ASC),
  INDEX `fk_group_shared_mags_1_group_idx` (`group_id` ASC),
  CONSTRAINT `fk_group_shared_mags_1_group`
    FOREIGN KEY (`group_id`)
    REFERENCES `halodb`.`group` (`id`),
  CONSTRAINT `fk_group_shared_mags_1_mags`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`mags` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;



-- -----------------------------------------------------
-- Table `halodb`.`user_shared_contigs_virus`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_shared_contigs_virus` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_shared_contigs_virus` (
  `user_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'owner\' is the propietary, can read and write and also delete the sample. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`user_id`, `shared_id`),
  INDEX `fk_user_has_contigs_virus_1_contigs_virus_idx` (`shared_id` ASC),
  INDEX `fk_user_has_contigs_virus_1_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_shared_contigs_virus_1_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  CONSTRAINT `fk_user_shared_contigs_virus_1_contigs_virus`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`contigs_virus` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`group_shared_contigs_virus`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group_shared_contigs_virus` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group_shared_contigs_virus` (
  `group_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'group\' is the group with some kind of access. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`group_id`, `shared_id`),
  INDEX `fk_group_shared_contigs_virus_1_contigs_virus_idx` (`shared_id` ASC),
  INDEX `fk_group_shared_contigs_virus_1_group_idx` (`group_id` ASC),
  CONSTRAINT `fk_group_shared_contigs_virus_1_group`
    FOREIGN KEY (`group_id`)
    REFERENCES `halodb`.`group` (`id`),
  CONSTRAINT `fk_group_shared_contigs_virus_1_contigs_virus`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`contigs_virus` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`user_shared_genome`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_shared_genome` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_shared_genome` (
  `user_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'owner\' is the propietary, can read and write and also delete the sample. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`user_id`, `shared_id`),
  INDEX `fk_user_has_genome_1_genome_idx` (`shared_id` ASC),
  INDEX `fk_user_has_genome_1_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_shared_genome_1_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  CONSTRAINT `fk_user_shared_genome_1_genome`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`genome` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`group_shared_genome`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group_shared_genome` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group_shared_genome` (
  `group_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'group\' is the group with some kind of access. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`group_id`, `shared_id`),
  INDEX `fk_group_shared_genome_1_genome_idx` (`shared_id` ASC),
  INDEX `fk_group_shared_genome_1_group_idx` (`group_id` ASC),
  CONSTRAINT `fk_group_shared_genome_1_group`
    FOREIGN KEY (`group_id`)
    REFERENCES `halodb`.`group` (`id`),
  CONSTRAINT `fk_group_shared_genome_1_genome`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`genome` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`user_shared_single_cell`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_shared_single_cell` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_shared_single_cell` (
  `user_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'owner\' is the propietary, can read and write and also delete the sample. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`user_id`, `shared_id`),
  INDEX `fk_user_has_single_cell_1_single_cell_idx` (`shared_id` ASC),
  INDEX `fk_user_has_single_cell_1_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_shared_single_cell_1_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  CONSTRAINT `fk_user_shared_single_cell_1_single_cell`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`single_cell` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`group_shared_single_cell`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group_shared_single_cell` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group_shared_single_cell` (
  `group_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'group\' is the group with some kind of access. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`group_id`, `shared_id`),
  INDEX `fk_group_shared_single_cell_1_single_cell_idx` (`shared_id` ASC),
  INDEX `fk_group_shared_single_cell_1_group_idx` (`group_id` ASC),
  CONSTRAINT `fk_group_shared_single_cell_1_group`
    FOREIGN KEY (`group_id`)
    REFERENCES `halodb`.`group` (`id`),
  CONSTRAINT `fk_group_shared_single_cell_1_single_cell`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`single_cell` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`user_shared_plasmid`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_shared_plasmid` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_shared_plasmid` (
  `user_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'owner\' is the propietary, can read and write and also delete the sample. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`user_id`, `shared_id`),
  INDEX `fk_user_has_plasmid_1_plasmid_idx` (`shared_id` ASC),
  INDEX `fk_user_has_plasmid_1_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_shared_plasmid_1_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  CONSTRAINT `fk_user_shared_plasmid_1_plasmid`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`plasmid` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`group_shared_plasmid`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group_shared_plasmid` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group_shared_plasmid` (
  `group_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  `access_mode` ENUM('read', 'readwrite')  NULL DEFAULT 'read' COMMENT "Describes the access mode to the sample. \'group\' is the group with some kind of access. \'read\' can read the data but no change it. \'readwrite\' can read and write but not delete.",
  PRIMARY KEY (`group_id`, `shared_id`),
  INDEX `fk_group_shared_plasmid_1_plasmid_idx` (`shared_id` ASC),
  INDEX `fk_group_shared_plasmid_1_group_idx` (`group_id` ASC),
  CONSTRAINT `fk_group_shared_plasmid_1_group`
    FOREIGN KEY (`group_id`)
    REFERENCES `halodb`.`group` (`id`),
  CONSTRAINT `fk_group_shared_plasmid_1_plasmid`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`plasmid` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;



-- -----------------------------------------------------
-- Table `halodb`.`housekeeping_shared_mags`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`housekeeping_shared_mags` ;

CREATE TABLE IF NOT EXISTS `halodb`.`housekeeping_shared_mags` (
  `hkgenes_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  PRIMARY KEY (`hkgenes_id`, `shared_id`),
  INDEX `fk_hkgenes_has_mags_1_mags_idx` (`shared_id` ASC),
  INDEX `fk_hkgenes_has_mags_1_hkgenes_idx` (`hkgenes_id` ASC),
  CONSTRAINT `fk_hkgenes_shared_mags_1_user`
    FOREIGN KEY (`hkgenes_id`)
    REFERENCES `halodb`.`hkgenes` (`id`),
  CONSTRAINT `fk_hkgenes_shared_mags_1_mags`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`mags` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`housekeeping_shared_genome`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`housekeeping_shared_genome` ;

CREATE TABLE IF NOT EXISTS `halodb`.`housekeeping_shared_genome` (
  `hkgenes_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  PRIMARY KEY (`hkgenes_id`, `shared_id`),
  INDEX `fk_hkgenes_has_genome_1_genome_idx` (`shared_id` ASC),
  INDEX `fk_hkgenes_has_genome_1_hkgenes_idx` (`hkgenes_id` ASC),
  CONSTRAINT `fk_hkgenes_shared_genome_1_user`
    FOREIGN KEY (`hkgenes_id`)
    REFERENCES `halodb`.`hkgenes` (`id`),
  CONSTRAINT `fk_hkgenes_shared_genome_1_genome`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`genome` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`housekeeping_shared_single_cell`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`housekeeping_shared_single_cell` ;

CREATE TABLE IF NOT EXISTS `halodb`.`housekeeping_shared_single_cell` (
  `hkgenes_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  PRIMARY KEY (`hkgenes_id`, `shared_id`),
  INDEX `fk_hkgenes_has_single_cell_1_single_cell_idx` (`shared_id` ASC),
  INDEX `fk_hkgenes_has_single_cell_1_hkgenes_idx` (`hkgenes_id` ASC),
  CONSTRAINT `fk_hkgenes_shared_single_cell_1_user`
    FOREIGN KEY (`hkgenes_id`)
    REFERENCES `halodb`.`hkgenes` (`id`),
  CONSTRAINT `fk_hkgenes_shared_single_cell_1_single_cell`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`single_cell` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`housekeeping_shared_plasmid`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`housekeeping_shared_plasmid` ;

CREATE TABLE IF NOT EXISTS `halodb`.`housekeeping_shared_plasmid` (
  `hkgenes_id` INT NOT NULL,
  `shared_id` INT NOT NULL,
  PRIMARY KEY (`hkgenes_id`, `shared_id`),
  INDEX `fk_hkgenes_has_plasmid_1_plasmid_idx` (`shared_id` ASC),
  INDEX `fk_hkgenes_has_plasmid_1_hkgenes_idx` (`hkgenes_id` ASC),
  CONSTRAINT `fk_hkgenes_shared_plasmid_1_user`
    FOREIGN KEY (`hkgenes_id`)
    REFERENCES `halodb`.`hkgenes` (`id`),
  CONSTRAINT `fk_hkgenes_shared_plasmid_1_plasmid`
    FOREIGN KEY (`shared_id`)
    REFERENCES `halodb`.`plasmid` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`sample_has_keywords`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`sample_has_keywords` ;

CREATE TABLE IF NOT EXISTS `halodb`.`sample_has_keywords` (
`sample_id` INT NOT NULL,
`keyword_id` INT NOT NULL,
PRIMARY KEY (`sample_id`, `keyword_id`),
INDEX `fk_sample_has_keywords_keyword_1_idx` (`keyword_id` ASC),
INDEX `fk_sample_has_keywords_sample_1_idx` (`sample_id` ASC),
CONSTRAINT `fk_sample_has_keywords_keyword_1`
  FOREIGN KEY (`keyword_id`)
      REFERENCES `halodb`.`keywords` (`id`),
CONSTRAINT `fk_sample_has_keywords_sample_1`
  FOREIGN KEY (`sample_id`)
      REFERENCES `halodb`.`sample` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `halodb`.`sample_has_dois`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`sample_has_dois` ;

CREATE TABLE IF NOT EXISTS `halodb`.`sample_has_dois` (
      `sample_id` INT NOT NULL,
      `doi_id` INT NOT NULL,
      PRIMARY KEY (`sample_id`, `doi_id`),
      INDEX `fk_sample_has_dois_doi_1_idx` (`doi_id` ASC),
      INDEX `fk_sample_has_dois_sample_1_idx` (`sample_id` ASC),
      CONSTRAINT `fk_sample_has_dois_doi_1`
          FOREIGN KEY (`doi_id`)
              REFERENCES `halodb`.`dois` (`id`),
      CONSTRAINT `fk_sample_has_dois_sample_1`
          FOREIGN KEY (`sample_id`)
              REFERENCES `halodb`.`sample` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- -----------------------------------------------------
-- -----------------------------------------------------


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
