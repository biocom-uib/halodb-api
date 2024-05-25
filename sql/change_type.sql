USE halodb;

ALTER TABLE `halodb`.`sample` 
CHANGE COLUMN `coverage` `coverage` FLOAT NULL DEFAULT NULL COMMENT 'Coverage (Nonpareil)' ;

ALTER TABLE `halodb`.`sample` 
CHANGE COLUMN `salo` `salo` FLOAT NULL DEFAULT NULL COMMENT 'Salinity optimum (0%-100%)' ;

ALTER TABLE `halodb`.`sample` 
CHANGE COLUMN `sals` `sals` FLOAT NULL DEFAULT NULL COMMENT 'Salinity of the sample [in percentage %]' ;

ALTER TABLE `halodb`.`sample` 
CHANGE COLUMN `ggcm` `ggcm` FLOAT NULL DEFAULT NULL COMMENT 'Molar percentage of Guanine and Cytosine in DNA.' ;

ALTER TABLE `halodb`.`sample` 
CHANGE COLUMN `contamination` `contamination` FLOAT NULL DEFAULT NULL COMMENT 'Level of contamination (0%-100%). Proportion of reads not belonging to MAGs detected. ' ;

ALTER TABLE `halodb`.`sample` 
CHANGE COLUMN `completeness` `completeness` FLOAT NULL DEFAULT NULL COMMENT 'Completeness (0%-100%). Percentage of the genome already processed.' ;

