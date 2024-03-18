<<<<<<< HEAD
CREATE DATABASE  IF NOT EXISTS `halodb` /*!40100 DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_bin */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `halodb`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: halodb
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `author`
--

DROP TABLE IF EXISTS `author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `author` (
  `id` int NOT NULL AUTO_INCREMENT,
  `author` varchar(80) COLLATE utf8mb3_bin DEFAULT NULL,
  `sample_id` int NOT NULL,
  `user_id` int NOT NULL,
  `corresponding_author` tinyint DEFAULT NULL,
  `email` varchar(256) COLLATE utf8mb3_bin DEFAULT NULL,
  PRIMARY KEY (`id`,`sample_id`),
  KEY `fk_authors_sample1_idx` (`sample_id`),
  KEY `fk_authors_user1_idx` (`user_id`),
  CONSTRAINT `fk_author_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_authors_sample1` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `experiment`
--

DROP TABLE IF EXISTS `experiment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiment` (
  `id` int NOT NULL,
  `name` varchar(80) COLLATE utf8mb3_bin NOT NULL,
  `description` varchar(400) COLLATE utf8mb3_bin DEFAULT NULL,
  `project_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_experiments_projects1_idx` (`project_id`),
  CONSTRAINT `fk_experiment_project` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fraction`
--

DROP TABLE IF EXISTS `fraction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fraction` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(40) COLLATE utf8mb3_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `group`
--

DROP TABLE IF EXISTS `group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group` (
  `id` int NOT NULL,
  `name` varchar(80) COLLATE utf8mb3_bin NOT NULL,
  `description` varchar(400) COLLATE utf8mb3_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `group_sharing_sample`
--

DROP TABLE IF EXISTS `group_sharing_sample`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group_sharing_sample` (
  `group_id` int NOT NULL,
  `sample_id` int NOT NULL,
  PRIMARY KEY (`group_id`,`sample_id`),
  KEY `fk_groups_has_samples_samples1_idx` (`sample_id`),
  KEY `fk_groups_has_samples_groups1_idx` (`group_id`),
  CONSTRAINT `fk_groups_has_samples_groups1` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`),
  CONSTRAINT `fk_groups_has_samples_samples1` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `keywords`
--

DROP TABLE IF EXISTS `keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `keywords` (
  `id` varchar(45) COLLATE utf8mb3_bin NOT NULL,
  `keyword` varchar(50) COLLATE utf8mb3_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `method`
--

DROP TABLE IF EXISTS `method`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `method` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(45) COLLATE utf8mb3_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `oxygen`
--

DROP TABLE IF EXISTS `oxygen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oxygen` (
  `id` int NOT NULL AUTO_INCREMENT,
  `relationship` varchar(40) COLLATE utf8mb3_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ph`
--

DROP TABLE IF EXISTS `ph`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ph` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(40) COLLATE utf8mb3_bin NOT NULL,
  `vmin` float DEFAULT NULL,
  `vmax` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project` (
  `id` int NOT NULL,
  `name` varchar(80) COLLATE utf8mb3_bin NOT NULL,
  `description` varchar(400) COLLATE utf8mb3_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `salinity`
--

DROP TABLE IF EXISTS `salinity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salinity` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(40) COLLATE utf8mb3_bin NOT NULL,
  `vmin` float DEFAULT NULL,
  `vmax` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sample`
--

DROP TABLE IF EXISTS `sample`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sample` (
  `experiment_id` int DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Sample unique internal identifier',
  `created` date DEFAULT NULL COMMENT 'Date created',
  `updated` date DEFAULT NULL COMMENT 'Date updated',
  `user_id` int DEFAULT NULL COMMENT 'User unique identifier, it''s a link to the user table',
  `txnr` int DEFAULT NULL COMMENT 'Taxonomic number',
  `version` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Version. NCBI accession & version',
  `entrydate` date DEFAULT NULL COMMENT 'Date of the entry',
  `firstdate` date DEFAULT NULL COMMENT 'First submission date',
  `draftnumber` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Draft number / date',
  `cult` enum('cultured','uncultured') CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Is the sample cultured or uncultured?',
  `koma` enum('isolate','MAG','SAG','virus','viral contig','plasmid') CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Kind of material',
  `typn` tinyint(1) DEFAULT NULL COMMENT 'Is this the designed type material for a new taxon? A true (1) or false (0) value',
  `otyp` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Type strain/MAG/SAG (in case of member of an extant taxon)',
  `txnt` int DEFAULT NULL COMMENT 'Taxonumber of the type material (in case of member of an extant taxon)',
  `ccsu` tinyint(1) DEFAULT NULL COMMENT 'If cultured, has been submitted to culture collection?  A true (1) or false (0) value',
  `type` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Designated type strain name/MAG/SAG (if TYPN is true)',
  `coln` varchar(80) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Strain collection numbers',
  `domain` varchar(25) COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Domain name',
  `kingdom` varchar(25) COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Kingdom name',
  `phylum` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Phylum name',
  `phylumety` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Phylum etymology',
  `class` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Class name',
  `classety` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Class etymology',
  `order` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Order  name',
  `orderety` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Order etymology',
  `family` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Family name',
  `familyety` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Family etymology',
  `gena` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Genus name',
  `gety` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Genus etymology',
  `gent` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Type species of the genus',
  `spep` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Specific epithet of the species',
  `spty` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Species etymology',
  `spna` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Species name',
  `baso` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Basonym',
  `ssna` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Subspecies name',
  `ssty` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Subspecies etymology',
  `coth` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Other comments',
  `titl` varchar(400) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Title',
  `jour` varchar(80) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Journal',
  `volume` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Volume',
  `pages` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Pages',
  `doi` varchar(400) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Publication DOI',
  `coau` varchar(80) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Corresponding autor',
  `emau` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'e-mail of the corresponding autor',
  `sixteensr` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT '16S rRNA gene accession number',
  `hkgn` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Alternative housekeeping genes',
  `meca` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Metagenome accession number',
  `gare` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'genome/MAG/SAG accession number [RefSeq/EMBL]',
  `gaem` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'genome/MAG/SAG accession number [EMBL]',
  `binn` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'genome/MAG/SAG accession number [other]',
  `url` varchar(400) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'URL',
  `gsta` enum('complete','partial','draft') CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Genome status',
  `completeness` decimal(10,0) DEFAULT NULL COMMENT 'Completeness percentage',
  `contamination` decimal(10,0) DEFAULT NULL COMMENT 'Level of contamination percentage',
  `method` int DEFAULT NULL COMMENT 'Method used to estimate completeness and contamination',
  `gsiz` int DEFAULT NULL COMMENT 'Estimated (for incomplete) or actual (for complete) genome or metagenome size. Unit bp (base pairs)',
  `ggcm` decimal(10,0) DEFAULT NULL COMMENT 'GC mol %',
  `dnae` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'DNA extraction method',
  `asem` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Assembly method',
  `seqt` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Sequencing Technology',
  `bins` varchar(80) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Binning software used and paràmetres',
  `asft` varchar(80) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Assembly software used and paràmetres',
  `coun` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Country of origin',
  `regi` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Region of origin',
  `geol` varchar(80) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Geographic location',
  `lati` float DEFAULT NULL COMMENT 'Latitude',
  `long` float DEFAULT NULL COMMENT 'Longitude',
  `alti` float DEFAULT NULL COMMENT 'Altitude in meters, over level at sea, where the sample was taken.',
  `dept` float DEFAULT NULL COMMENT 'Depth, in meters, where the sample was taken, with respect to the fild alti. That is, if the sample was taken in a lake placed on a mountain, alti contains the altitude of the lake''s surface and dept represents the depth into the lake where the sample was taken.',
  `sour` varchar(80) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Source of sample',
  `dats` date DEFAULT NULL COMMENT 'Sampling date',
  `hocs` time DEFAULT NULL COMMENT 'Hour of collection of the sample [sharp hours]',
  `dati` date DEFAULT NULL COMMENT 'Date of isolation',
  `datu` date DEFAULT NULL COMMENT 'Date of isolation if unknown',
  `tems` float DEFAULT NULL COMMENT 'Temperature of the sample [in celsius degrees]',
  `phsa` float DEFAULT NULL COMMENT 'pH of the sample',
  `sals` decimal(10,0) DEFAULT NULL COMMENT 'Salinity of the sample [in percentage %]',
  `emet` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Energy metabolism',
  `orel` int DEFAULT NULL COMMENT 'Relationship to O2. It''s a foreign key for oxygen table',
  `elac` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Terminal electron acceptor',
  `temo` float DEFAULT NULL COMMENT 'Temperature optimum',
  `teml` float DEFAULT NULL COMMENT 'Lowest temperature for growth',
  `temh` float DEFAULT NULL COMMENT 'Highest temperature for growth',
  `temc` int DEFAULT NULL COMMENT 'Temperature category. It''s a foreign key for temperature table',
  `phop` float DEFAULT NULL COMMENT 'pH optimum',
  `phlo` float DEFAULT NULL COMMENT 'Lowest pH for growth',
  `phhi` float DEFAULT NULL COMMENT 'Highest pH for growth',
  `phca` int DEFAULT NULL COMMENT 'pH category. It''s a foreign key for ph table',
  `salo` decimal(10,0) DEFAULT NULL COMMENT 'Salinity optimum percentage',
  `sall` decimal(10,0) DEFAULT NULL COMMENT 'Lowest NaCl concentration percentage for growth',
  `salh` decimal(10,0) DEFAULT NULL COMMENT 'Highest NaCl concentration percentage for growth',
  `salw` varchar(80) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Other salts besides NaCl to be reported',
  `salc` int DEFAULT NULL COMMENT 'Salinity category. It''s a foreign key for salinity table',
  `bios` enum('BSL-1','BSL-2','BSL-3','BSL-4') CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Biosafety level',
  `habt` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Habitat of the sample',
  `bior` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Biotic relationship',
  `host` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Symbiosis with the host',
  `path` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Known pathogenicity',
  `extr` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Miscellaneous, extraordinary features relevant for the description',
  `name` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Sample name',
  `stype` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Sample type',
  `ssize` float DEFAULT NULL COMMENT 'Sample size',
  `ssizeunit` enum('μl','ml','l','g','Kg') CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Sample size units',
  `sfrac` int DEFAULT NULL COMMENT 'Sequenced fraction. It''s a foreign key for fraction table',
  `target` int DEFAULT NULL COMMENT 'Target nucleic acids. It''s a foreign key for target table',
  `rreads` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Raw reads. An uuid unique identifier of the file into the server''s filesystem.',
  `rreadacc` int DEFAULT NULL COMMENT 'Raw reads NCBI accesion code',
  `rrname` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Name of the original file containing the raw reads',
  `rreadsnum` int DEFAULT NULL COMMENT 'Amount of raw reads. Unit: bp (base pairs)',
  `treads` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Trimmed reads. An uuid unique identifier of the file into the server''s filesystem.',
  `trname` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Name of the original file containing the trimmed reads',
  `treadsnum` int DEFAULT NULL COMMENT 'Amount of trimmed reads. Unit: bp (base pairs)',
  `coverage` decimal(10,0) DEFAULT NULL COMMENT 'Coverage percentage (Nonpareil)',
  `assembled` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Assembly file. An uuid unique identifier of the file into the server''s filesystem.',
  `assname` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Name of the original file containing the assembly',
  `asize` int DEFAULT NULL COMMENT 'Assembly size. Unit: bp (base pairs)',
  `contignumber` int DEFAULT NULL COMMENT 'Number of contigs',
  `pgenes` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Predicted genes. An uuid unique identifier of the file into the server''s filesystem.',
  `pgenesname` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Name of the original file containing the predicted names',
  `seqdepth` float DEFAULT NULL COMMENT 'Sequencing depth (Isolates/MAG)',
  `twentythreesr` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT '23S rRNA gene accession number',
  `nagoya` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Information related to the Nagoya Protocol',
  `sequrl` varchar(400) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'Sequence URL',
  PRIMARY KEY (`id`),
  KEY `fk_samples_experiments1_idx` (`experiment_id`),
  KEY `fk_samples_users1_idx` (`user_id`),
  KEY `fk_samples_oxygen1_idx` (`orel`),
  KEY `fk_samples_temperature1_idx` (`temc`),
  KEY `fk_samples_ph1_idx` (`phca`),
  KEY `fk_samples_salinity1_idx` (`salc`),
  KEY `fk_samples_fraction1_idx` (`sfrac`),
  KEY `fk_samples_target1_idx` (`target`),
  KEY `fk_sample_method1_idx` (`method`),
  CONSTRAINT `fk_sample_method1` FOREIGN KEY (`method`) REFERENCES `method` (`id`),
  CONSTRAINT `fk_samples_experiments1` FOREIGN KEY (`experiment_id`) REFERENCES `experiment` (`id`),
  CONSTRAINT `fk_samples_fraction1` FOREIGN KEY (`sfrac`) REFERENCES `fraction` (`id`),
  CONSTRAINT `fk_samples_oxygen1` FOREIGN KEY (`orel`) REFERENCES `oxygen` (`id`),
  CONSTRAINT `fk_samples_ph1` FOREIGN KEY (`phca`) REFERENCES `ph` (`id`),
  CONSTRAINT `fk_samples_salinity1` FOREIGN KEY (`salc`) REFERENCES `salinity` (`id`),
  CONSTRAINT `fk_samples_target1` FOREIGN KEY (`target`) REFERENCES `target` (`id`),
  CONSTRAINT `fk_samples_temperature1` FOREIGN KEY (`temc`) REFERENCES `temperature` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sample_has_keywords`
--

DROP TABLE IF EXISTS `sample_has_keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sample_has_keywords` (
  `sample_id` int NOT NULL,
  `keywords_id` varchar(45) COLLATE utf8mb3_bin NOT NULL,
  PRIMARY KEY (`sample_id`,`keywords_id`),
  KEY `fk_sample_has_keywords_keywords1_idx` (`keywords_id`),
  KEY `fk_sample_has_keywords_sample1_idx` (`sample_id`),
  CONSTRAINT `fk_sample_has_keywords_keywords1` FOREIGN KEY (`keywords_id`) REFERENCES `keywords` (`id`),
  CONSTRAINT `fk_sample_has_keywords_sample1` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `target`
--

DROP TABLE IF EXISTS `target`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `target` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) COLLATE utf8mb3_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temperature`
--

DROP TABLE IF EXISTS `temperature`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temperature` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(40) COLLATE utf8mb3_bin NOT NULL,
  `vmin` float DEFAULT NULL,
  `vmax` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` varchar(40) COLLATE utf8mb3_bin NOT NULL COMMENT 'Firebase unique identifier',
  `name` varchar(80) COLLATE utf8mb3_bin NOT NULL,
  `surname` varchar(80) COLLATE utf8mb3_bin DEFAULT NULL,
  `email` varchar(256) COLLATE utf8mb3_bin NOT NULL,
  `password` varchar(100) COLLATE utf8mb3_bin NOT NULL,
  `registration_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid_UNIQUE` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_experiment`
--

DROP TABLE IF EXISTS `user_experiment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_experiment` (
  `user_id` int NOT NULL,
  `experiment_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`experiment_id`),
  KEY `fk_users_has_experiments_experiments1_idx` (`experiment_id`),
  KEY `fk_users_has_experiments_users1_idx` (`user_id`),
  CONSTRAINT `fk_user_experiment_experiment1` FOREIGN KEY (`experiment_id`) REFERENCES `experiment` (`id`),
  CONSTRAINT `fk_user_experiment_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_has_group`
--

DROP TABLE IF EXISTS `user_has_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_has_group` (
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`group_id`),
  KEY `fk_users_has_groups_groups1_idx` (`group_id`),
  KEY `fk_users_has_groups_users_idx` (`user_id`),
  CONSTRAINT `fk_user_has_group_group1` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`),
  CONSTRAINT `fk_users_has_groups_users` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_project`
--

DROP TABLE IF EXISTS `user_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_project` (
  `user_id` int NOT NULL,
  `project_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`project_id`),
  KEY `fk_users_has_projects_projects1_idx` (`project_id`),
  KEY `fk_users_has_projects_users1_idx` (`user_id`),
  CONSTRAINT `fk_user_project_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_users_has_projects_projects1` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_shared_sample`
--

DROP TABLE IF EXISTS `user_shared_sample`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_shared_sample` (
  `user_id` int NOT NULL,
  `sample_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`sample_id`),
  KEY `fk_users_has_samples_samples1_idx` (`sample_id`),
  KEY `fk_users_has_samples_users1_idx` (`user_id`),
  CONSTRAINT `fk_user_shared_sample_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_users_has_samples_samples1` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-16 19:26:20
=======
-- MySQL Script generated by MySQL Workbench
-- Fri Mar  8 00:12:20 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `halodb` ;
-- -----------------------------------------------------
-- Schema HaloDB
--
-- The HaloDB 
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `halodb` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;
-- -----------------------------------------------------
-- Schema halodb
-- -----------------------------------------------------

USE `halodb` ;

-- -----------------------------------------------------
-- Table `HaloDB`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`user` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `uid` VARCHAR(40) NOT NULL COMMENT 'Firebase unique identifier',
  `name` VARCHAR(80) COLLATE 'utf8mb3_bin' NOT NULL,
  `surname` VARCHAR(80) COLLATE 'utf8mb3_bin' NULL,
  `email` VARCHAR(256) COLLATE 'utf8mb3_bin' NOT NULL,
  `password` VARCHAR(100) COLLATE 'utf8mb3_bin' NOT NULL,
  `registration_time` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`group`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`group` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`group` (
  `id` INT NOT NULL,
  `name` VARCHAR(80) COLLATE 'utf8mb3_bin' NOT NULL,
  `description` VARCHAR(400) COLLATE 'utf8mb3_bin' NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`user_has_group`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`user_has_group` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`user_has_group` (
  `user_id` INT NOT NULL,
  `group_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `group_id`),
  INDEX `fk_users_has_groups_groups1_idx` (`group_id` ASC),
  INDEX `fk_users_has_groups_users_idx` (`user_id` ASC),
  CONSTRAINT `fk_users_has_groups_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `HaloDB`.`user` (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`project`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`project` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`project` (
  `id` INT NOT NULL,
  `name` VARCHAR(80) COLLATE 'utf8mb3_bin' NOT NULL,
  `description` VARCHAR(400) COLLATE 'utf8mb3_bin' NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`experiment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`experiment` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`experiment` (
  `id` INT NOT NULL,
  `name` VARCHAR(80) COLLATE 'utf8mb3_bin' NOT NULL,
  `description` VARCHAR(400) COLLATE 'utf8mb3_bin' NULL,
  `project_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_experiments_projects1_idx` (`project_id` ASC),
  CONSTRAINT `fk_experiment_project`
    FOREIGN KEY (`project_id`)
    REFERENCES `HaloDB`.`project` (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`fraction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`fraction` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`fraction` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(40) COLLATE 'utf8mb3_bin' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`oxygen`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`oxygen` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`oxygen` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `relationship` VARCHAR(40) COLLATE 'utf8mb3_bin' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`ph`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`ph` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`ph` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(40) COLLATE 'utf8mb3_bin' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`salinity`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`salinity` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`salinity` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(40) COLLATE 'utf8mb3_bin' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`target`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`target` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`target` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) COLLATE 'utf8mb3_bin' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`temperature`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`temperature` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`temperature` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(40) COLLATE 'utf8mb3_bin' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`method`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`method` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`method` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`sample`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`sample` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`sample` (
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
    REFERENCES `HaloDB`.`experiment` (`id`),
  CONSTRAINT `fk_samples_fraction1`
    FOREIGN KEY (`sfrac`)
    REFERENCES `HaloDB`.`fraction` (`id`),
  CONSTRAINT `fk_samples_oxygen1`
    FOREIGN KEY (`orel`)
    REFERENCES `HaloDB`.`oxygen` (`id`),
  CONSTRAINT `fk_samples_ph1`
    FOREIGN KEY (`phca`)
    REFERENCES `HaloDB`.`ph` (`id`),
  CONSTRAINT `fk_samples_salinity1`
    FOREIGN KEY (`salc`)
    REFERENCES `HaloDB`.`salinity` (`id`),
  CONSTRAINT `fk_samples_target1`
    FOREIGN KEY (`target`)
    REFERENCES `HaloDB`.`target` (`id`),
  CONSTRAINT `fk_samples_temperature1`
    FOREIGN KEY (`temc`)
    REFERENCES `HaloDB`.`temperature` (`id`),
  CONSTRAINT `fk_sample_method1`
    FOREIGN KEY (`method`)
    REFERENCES `HaloDB`.`method` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`user_shared_sample`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`user_shared_sample` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`user_shared_sample` (
  `user_id` INT NOT NULL,
  `sample_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `sample_id`),
  INDEX `fk_users_has_samples_samples1_idx` (`sample_id` ASC),
  INDEX `fk_users_has_samples_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_users_has_samples_samples1`
    FOREIGN KEY (`sample_id`)
    REFERENCES `HaloDB`.`sample` (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`group_sharing_sample`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`group_sharing_sample` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`group_sharing_sample` (
  `group_id` INT NOT NULL,
  `sample_id` INT NOT NULL,
  PRIMARY KEY (`group_id`, `sample_id`),
  INDEX `fk_groups_has_samples_samples1_idx` (`sample_id` ASC),
  INDEX `fk_groups_has_samples_groups1_idx` (`group_id` ASC),
  CONSTRAINT `fk_groups_has_samples_groups1`
    FOREIGN KEY (`group_id`)
    REFERENCES `HaloDB`.`group` (`id`),
  CONSTRAINT `fk_groups_has_samples_samples1`
    FOREIGN KEY (`sample_id`)
    REFERENCES `HaloDB`.`sample` (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`user_experiment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`user_experiment` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`user_experiment` (
  `user_id` INT NOT NULL,
  `experiment_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `experiment_id`),
  INDEX `fk_users_has_experiments_experiments1_idx` (`experiment_id` ASC),
  INDEX `fk_users_has_experiments_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_experiment_experiment1`
    FOREIGN KEY (`experiment_id`)
    REFERENCES `HaloDB`.`experiment` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`user_project`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`user_project` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`user_project` (
  `user_id` INT NOT NULL,
  `project_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `project_id`),
  INDEX `fk_users_has_projects_projects1_idx` (`project_id` ASC),
  INDEX `fk_users_has_projects_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_users_has_projects_projects1`
    FOREIGN KEY (`project_id`)
    REFERENCES `HaloDB`.`project` (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`author`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`author` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`author` (
  `author` VARCHAR(80) COLLATE 'utf8mb3_bin' NULL,
  `sample_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `corresponding_author` TINYINT NULL,
  `email` VARCHAR(256) COLLATE 'utf8mb3_bin' NULL,
  PRIMARY KEY (`sample_id`),
  INDEX `fk_authors_sample1_idx` (`sample_id` ASC),
  INDEX `fk_authors_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_authors_sample1`
    FOREIGN KEY (`sample_id`)
    REFERENCES `HaloDB`.`sample` (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`keywords`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`keywords` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`keywords` (
  `id` VARCHAR(45) COLLATE 'utf8mb3_bin' NOT NULL,
  `keyword` VARCHAR(50) COLLATE 'utf8mb3_bin' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HaloDB`.`sample_has_keywords`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `HaloDB`.`sample_has_keywords` ;

CREATE TABLE IF NOT EXISTS `HaloDB`.`sample_has_keywords` (
  `sample_id` INT NOT NULL,
  `keywords_id` VARCHAR(45) COLLATE 'utf8mb3_bin' NOT NULL,
  PRIMARY KEY (`sample_id`, `keywords_id`),
  INDEX `fk_sample_has_keywords_keywords1_idx` (`keywords_id` ASC),
  INDEX `fk_sample_has_keywords_sample1_idx` (`sample_id` ASC),
  CONSTRAINT `fk_sample_has_keywords_keywords1`
    FOREIGN KEY (`keywords_id`)
    REFERENCES `HaloDB`.`keywords` (`id`),
  CONSTRAINT `fk_sample_has_keywords_sample1`
    FOREIGN KEY (`sample_id`)
    REFERENCES `HaloDB`.`sample` (`id`))
ENGINE = InnoDB;

USE `halodb` ;

-- -----------------------------------------------------
-- Table `halodb`.`project`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`project` ;

CREATE TABLE IF NOT EXISTS `halodb`.`project` (
  `id` INT NOT NULL,
  `name` VARCHAR(80) COLLATE 'utf8mb3_bin' NOT NULL,
  `description` VARCHAR(400) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`experiment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`experiment` ;

CREATE TABLE IF NOT EXISTS `halodb`.`experiment` (
  `id` INT NOT NULL,
  `name` VARCHAR(80) COLLATE 'utf8mb3_bin' NOT NULL,
  `description` VARCHAR(400) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL,
  `project_id` INT NOT NULL,
  PRIMARY KEY (`id`, `project_id`),
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
-- Table `halodb`.`group`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group` (
  `id` INT NOT NULL,
  `name` VARCHAR(80) COLLATE 'utf8mb3_bin' NOT NULL,
  `description` VARCHAR(400) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(80) COLLATE 'utf8mb3_bin' NOT NULL,
  `surname` VARCHAR(80) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL,
  `email` VARCHAR(256) COLLATE 'utf8mb3_bin' NOT NULL,
  `password` VARCHAR(100) COLLATE 'utf8mb3_bin' NOT NULL,
  `registration_time` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
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
-- Table `halodb`.`temperature`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`temperature` ;

CREATE TABLE IF NOT EXISTS `halodb`.`temperature` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(40) COLLATE 'utf8mb3_bin' NOT NULL,
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
  `txnr` INT NULL DEFAULT NULL COMMENT 'Taxonomic number',
  `version` VARCHAR(20) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Version. NCBI accession & version',
  `entrydate` DATE NULL DEFAULT NULL COMMENT 'Date of the entry',
  `firstdate` DATE NULL DEFAULT NULL COMMENT 'First submission date',
  `draftnumber` VARCHAR(8) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Draft number / date',
  `cult` ENUM('cultured', 'uncultured') COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Is the sample cultured or uncultured?',
  `koma` ENUM('isolate', 'MAG', 'SAG', 'virus', 'viral contig', 'plasmid') COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Kind of material',
  `typn` TINYINT(1) NULL DEFAULT NULL COMMENT 'Is this the designed type material for a new taxon? A true (1) or false (0) value',
  `otyp` VARCHAR(30) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Type strain/MAG/SAG (in case of member of an extant taxon)',
  `txnt` INT NULL DEFAULT NULL COMMENT 'Taxonumber of the type material (in case of member of an extant taxon)',
  `ccsu` TINYINT(1) NULL DEFAULT NULL COMMENT 'If cultured, has been submitted to culture collection?  A true (1) or false (0) value',
  `type` VARCHAR(30) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Designated type strain name/MAG/SAG (if TYPN is true)',
  `coln` VARCHAR(80) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Strain collection numbers',
  `phylum` VARCHAR(50) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Phylum name',
  `phylumety` VARCHAR(256) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Phylum etymology',
  `class` VARCHAR(50) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Class name',
  `classety` VARCHAR(256) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Class etymology',
  `order` VARCHAR(50) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Order  name',
  `orderety` VARCHAR(256) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Order etymology',
  `family` VARCHAR(50) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Family name',
  `familyety` VARCHAR(256) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Family etymology',
  `gena` VARCHAR(50) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Genus name',
  `gety` VARCHAR(256) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Genus etymology',
  `gent` VARCHAR(50) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Type species of the genus',
  `spep` VARCHAR(50) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Specific epithet of the species',
  `spty` VARCHAR(256) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Species etymology',
  `spna` VARCHAR(50) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Species name',
  `baso` VARCHAR(50) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Basonym',
  `ssna` VARCHAR(50) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Subspecies name',
  `ssty` VARCHAR(50) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Subspecies etymology',
  `coth` VARCHAR(500) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Other comments',
  `titl` VARCHAR(400) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Title',
  `jour` VARCHAR(80) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Journal',
  `volume` VARCHAR(20) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Volume',
  `pages` VARCHAR(20) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Pages',
  `doi` VARCHAR(400) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Publication DOI',
  `coau` VARCHAR(80) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Corresponding autor',
  `emau` VARCHAR(256) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'e-mail of the corresponding autor',
  `sixteensr` VARCHAR(20) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT '16S rRNA gene accession number',
  `hkgn` VARCHAR(20) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Alternative housekeeping genes',
  `meca` VARCHAR(20) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Metagenome accession number',
  `gare` VARCHAR(20) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'genome/MAG/SAG accession number [RefSeq/EMBL]',
  `gaem` VARCHAR(20) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'genome/MAG/SAG accession number [EMBL]',
  `binn` VARCHAR(20) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'genome/MAG/SAG accession number [other]',
  `url` VARCHAR(400) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'URL',
  `gsta` ENUM('complete', 'partial', 'draft') COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Genome status',
  `completeness` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'Completeness percentage',
  `contamination` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'Level of contamination percentage',
  `method` INT NULL DEFAULT NULL COMMENT 'Method used to estimate completeness and contamination',
  `gsiz` INT NULL DEFAULT NULL COMMENT 'Estimated (for incomplete) or actual (for complete) genome or metagenome size. Unit bp (base pairs)',
  `ggcm` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'GC mol %',
  `dnae` VARCHAR(40) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'DNA extraction method',
  `asem` VARCHAR(40) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Assembly method',
  `seqt` VARCHAR(40) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Sequencing Technology',
  `bins` VARCHAR(80) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Binning software used and paràmetres',
  `asft` VARCHAR(80) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Assembly software used and paràmetres',
  `coun` VARCHAR(30) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Country of origin',
  `regi` VARCHAR(30) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Region of origin',
  `geol` VARCHAR(80) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Geographic location',
  `lati` FLOAT NULL DEFAULT NULL COMMENT 'Latitude',
  `long` FLOAT NULL DEFAULT NULL COMMENT 'Longitude',
  `alti` FLOAT NULL DEFAULT NULL COMMENT 'Altitude in meters, over level at sea, where the sample was taken.',
  `dept` FLOAT NULL DEFAULT NULL COMMENT 'Depth, in meters, where the sample was taken, with respect to the fild alti. That is, if the sample was taken in a lake placed on a mountain, alti contains the altitude of the lake\'s surface and dept represents the depth into the lake where the sample was taken.',
  `sour` VARCHAR(80) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Source of sample',
  `dats` DATE NULL DEFAULT NULL COMMENT 'Sampling date',
  `hocs` TIME NULL DEFAULT NULL COMMENT 'Hour of collection of the sample [sharp hours]',
  `dati` DATE NULL DEFAULT NULL COMMENT 'Date of isolation',
  `datu` DATE NULL DEFAULT NULL COMMENT 'Date of isolation if unknown',
  `tems` FLOAT NULL DEFAULT NULL COMMENT 'Temperature of the sample [in celsius degrees]',
  `phsa` FLOAT NULL DEFAULT NULL COMMENT 'pH of the sample',
  `sals` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'Salinity of the sample [in percentage %]',
  `emet` VARCHAR(500) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Energy metabolism',
  `orel` INT NULL DEFAULT NULL COMMENT 'Relationship to O2. It\'s a foreign key for oxygen table',
  `elac` VARCHAR(40) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Terminal electron acceptor',
  `temo` FLOAT NULL DEFAULT NULL COMMENT 'Temperature optimum',
  `teml` FLOAT NULL DEFAULT NULL COMMENT 'Lowest temperature for growth',
  `temh` FLOAT NULL DEFAULT NULL COMMENT 'Highest temperature for growth',
  `temc` INT NULL DEFAULT NULL COMMENT 'Temperature category. It\'s a foreign key for temperature table',
  `phop` FLOAT NULL DEFAULT NULL COMMENT 'pH optimum',
  `phlo` FLOAT NULL DEFAULT NULL COMMENT 'Lowest pH for growth',
  `phhi` FLOAT NULL DEFAULT NULL COMMENT 'Highest pH for growth',
  `phca` INT NULL DEFAULT NULL COMMENT 'pH category. It\'s a foreign key for ph table',
  `salo` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'Salinity optimum percentage',
  `sall` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'Lowest NaCl concentration percentage for growth',
  `salh` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'Highest NaCl concentration percentage for growth',
  `salw` VARCHAR(80) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Other salts besides NaCl to be reported',
  `salc` INT NULL DEFAULT NULL COMMENT 'Salinity category. It\'s a foreign key for salinity table',
  `bios` ENUM('BSL-1', 'BSL-2', 'BSL-3', 'BSL-4') COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Biosafety level',
  `habt` VARCHAR(100) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Habitat of the sample',
  `bior` VARCHAR(100) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Biotic relationship',
  `host` VARCHAR(100) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Symbiosis with the host',
  `path` VARCHAR(200) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Known pathogenicity',
  `extr` VARCHAR(500) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Miscellaneous, extraordinary features relevant for the description',
  `name` VARCHAR(100) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Sample name',
  `stype` VARCHAR(200) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Sample type',
  `ssize` FLOAT NULL DEFAULT NULL COMMENT 'Sample size',
  `ssizeunit` ENUM('μl', 'ml', 'l', 'g', 'Kg') COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Sample size units',
  `sfrac` INT NULL DEFAULT NULL COMMENT 'Sequenced fraction. It\'s a foreign key for fraction table',
  `target` INT NULL DEFAULT NULL COMMENT 'Target nucleic acids. It\'s a foreign key for target table',
  `rreads` VARCHAR(40) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Raw reads. An uuid unique identifier of the file into the server\'s filesystem.',
  `rreadacc` INT NULL DEFAULT NULL COMMENT 'Raw reads NCBI accesion code',
  `rrname` VARCHAR(100) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Name of the original file containing the raw reads',
  `rreadsnum` INT NULL DEFAULT NULL COMMENT 'Amount of raw reads. Unit: bp (base pairs)',
  `treads` VARCHAR(40) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Trimmed reads. An uuid unique identifier of the file into the server\'s filesystem.',
  `trname` VARCHAR(100) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Name of the original file containing the trimmed reads',
  `treadsnum` INT NULL DEFAULT NULL COMMENT 'Amount of trimmed reads. Unit: bp (base pairs)',
  `coverage` DECIMAL(10,0) NULL DEFAULT NULL COMMENT 'Coverage percentage (Nonpareil)',
  `assembled` VARCHAR(40) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Assembly file. An uuid unique identifier of the file into the server\'s filesystem.',
  `assname` VARCHAR(100) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Name of the original file containing the assembly',
  `asize` INT NULL DEFAULT NULL COMMENT 'Assembly size. Unit: bp (base pairs)',
  `contignumber` INT NULL DEFAULT NULL COMMENT 'Number of contigs',
  `pgenes` VARCHAR(40) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Predicted genes. An uuid unique identifier of the file into the server\'s filesystem.',
  `pgenesname` VARCHAR(100) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Name of the original file containing the predicted names',
  `seqdepth` FLOAT NULL DEFAULT NULL COMMENT 'Sequencing depth (Isolates/MAG)',
  `twentythreesr` VARCHAR(20) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT '23S rRNA gene accession number',
  `nagoya` VARCHAR(500) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Information related to the Nagoya Protocol',
  `sequrl` VARCHAR(400) COLLATE 'utf8mb3_bin' NULL DEFAULT NULL COMMENT 'Sequence URL',
  `temperature_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_samples_experiments1_idx` (`experiment_id` ASC),
  INDEX `fk_samples_users1_idx` (`user_id` ASC),
  INDEX `fk_sample_oxygen1_idx` (`orel` ASC),
  INDEX `fk_sample_temperature1_idx` (`temperature_id` ASC),
  CONSTRAINT `fk_samples_experiments1`
    FOREIGN KEY (`experiment_id`)
    REFERENCES `halodb`.`experiment` (`id`),
  CONSTRAINT `fk_samples_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`),
  CONSTRAINT `fk_sample_oxygen1`
    FOREIGN KEY (`orel`)
    REFERENCES `halodb`.`oxygen` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_sample_temperature1`
    FOREIGN KEY (`temperature_id`)
    REFERENCES `halodb`.`temperature` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`group_sharing_sample`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`group_sharing_sample` ;

CREATE TABLE IF NOT EXISTS `halodb`.`group_sharing_sample` (
  `group_id` INT NOT NULL,
  `sample_id` INT NOT NULL,
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
-- Table `halodb`.`keywords`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`keywords` ;

CREATE TABLE IF NOT EXISTS `halodb`.`keywords` (
  `id` VARCHAR(45) COLLATE 'utf8mb3_bin' NOT NULL,
  `keyword` VARCHAR(50) COLLATE 'utf8mb3_bin' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`ph`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`ph` ;

CREATE TABLE IF NOT EXISTS `halodb`.`ph` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(40) COLLATE 'utf8mb3_bin' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`salinity`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`salinity` ;

CREATE TABLE IF NOT EXISTS `halodb`.`salinity` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(40) COLLATE 'utf8mb3_bin' NOT NULL,
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
-- Table `halodb`.`user_experiment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_experiment` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_experiment` (
  `user_id` INT NOT NULL,
  `experiment_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `experiment_id`),
  INDEX `fk_users_has_experiments_experiments1_idx` (`experiment_id` ASC),
  INDEX `fk_users_has_experiments_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_users_has_experiments_experiments1`
    FOREIGN KEY (`experiment_id`)
    REFERENCES `halodb`.`experiment` (`id`),
  CONSTRAINT `fk_users_has_experiments_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`user_has_group`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_has_group` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_has_group` (
  `user_id` INT NOT NULL,
  `group_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `group_id`),
  INDEX `fk_users_has_groups_groups1_idx` (`group_id` ASC),
  INDEX `fk_users_has_groups_users_idx` (`user_id` ASC),
  CONSTRAINT `fk_users_has_groups_groups1`
    FOREIGN KEY (`group_id`)
    REFERENCES `halodb`.`group` (`id`),
  CONSTRAINT `fk_users_has_groups_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`))
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
  CONSTRAINT `fk_users_has_projects_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `halodb`.`user_shared_sample`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `halodb`.`user_shared_sample` ;

CREATE TABLE IF NOT EXISTS `halodb`.`user_shared_sample` (
  `user_id` INT NOT NULL,
  `sample_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `sample_id`),
  INDEX `fk_users_has_samples_samples1_idx` (`sample_id` ASC),
  INDEX `fk_users_has_samples_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_users_has_samples_samples1`
    FOREIGN KEY (`sample_id`)
    REFERENCES `halodb`.`sample` (`id`),
  CONSTRAINT `fk_users_has_samples_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `halodb`.`user` (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
>>>>>>> main
