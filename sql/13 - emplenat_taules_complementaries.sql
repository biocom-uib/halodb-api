
USE `HaloDB` ;


insert into method (description) values
("BUSCO"),
("CheckM"),
("OrthoDB"),
("Kraken"),
("BlobTools"),
("Anvi’o "),
("MiGA");


insert into oxygen (description) values 
("Aerobic metabolism"), 
("Obligate Anaerobic metabolism"), 
("Facultative Anaerobic metabolism"), 
("Microarophiles"), 
("Aerotolerant anaerobes");


insert into temperature (id, description, vmin, vmax) values 
(1, "Psychrophyles (-20ºC, 10ºC]", '-20.0', '10.0'),
(2, "Mesophiles (10ºC, 45ºC]", '10.0', '45.0'),
(3, "Moderate thermophiles (45ºC, 60ºC]", '45.0', '60.0'),
(4, "Thermophiles (60ºC, 80ºC]", '60.0', '80.0'),
(5, "Hyperthermophiles (80ºC, 122ºC)", '80.0', '122.0');


insert into ph (id, description, vmin, vmax) values 
( 1, "Ultra acidic (-∞, 3.5]", '-3.402823466E+38', '3.5'),
( 2, "Extremely acidic (3.5, 4.5]", '3.5', '4.5'),
( 3, "Very strongly acidic (4.5, 5.0]", '4.5', '5.0'),
( 4, "Strongly acidic (5.0, 5.5]", '5.0', '5.5'),
( 5, "Moderately acidic (5.5, 6.0]", '5.5', '6.0'),
( 6, "Slightly acidic (6.0, 6.5]", '6.0', '6.5'),
( 7, "Neutral (6.5, 7.3]", '6.5', '7.3'),
( 8, "Slightly alkaline (7.3, 7.8]", '7.3', '7.8'),
( 9, "Moderately alkaline (7.8, 8.4]", '7.8', '8.4'),
(10, "Strongly alkaline (8.4, 9.0]", '8.4', '9.0'),
(11, "Very strongly alkaline (9.0, 10.5]", '9.0', '10.5'),
(12, "Hyper alkaline (10.5, +∞)", '10.5', '3.402823466E+38');

insert into salinity (id, description, vmin, vmax) values
(1, "Halotolerants [0%, 1%]", "0.0", "1.0"), 
(2, "slight halophiles (1%, 3%]", "1.0", "3.0"),
(3, "Moderate halophiles (3%, 15%]", "3.0", "15.0"),
(4, "Extreme halophiles (15%, 32%]", "15.0", "32.0");

-- ######################################## 
-- insert into salinity (description) values
-- ("Oligohaline [0.5‰, 5‰]"),
-- ("Mesohaline (5‰, 18‰]"),
-- ("Polyhaline (18‰, 30‰]"),
-- ("Euhaline (30‰, 45‰]"),
-- ("Metahaline (45‰, 65‰]"),
-- ("Hyperhaline (65 ‰, +∞)");
-- ########################################

-- ########################################
--  Convertit a enum
-- insert into biosafety (description) values
-- ("BSL-1"),
-- ("BSL-2"),
-- ("BSL-3"),
-- ("BSL-4");
-- ########################################

insert into fraction (description) values
("Genome"),
("MAG"),
("SAG"),
("Virus"),
("Virome"),
("Transcriptome"),
("Exome"),
("Microbiome"),
("Epigenome"),
("Metabolome"),
("Meta-epigenome"),
("Metagenome"),
("Metaphenome"),
("Metaproteome"),
("Metavirome"),
("Metatranscriptome"),
("Targeted Sequencing"),
("Chromatin Conformation Capture"),
("Phageome"),
("Plasmids and Mobile Genetic Elements");



insert into target (description) values
("gDNA (genomic DNA)"),
("Exome"),
("mtDNA (mitochondrial DNA)"),
("cpDNA (Chloroplast DNA)"),
("mRNA (Messenger RNA)"),
("tRNA (Transfer RNA)"),
("ncRNA (Non-coding RNA)"),
("RNA (total RNA)");


insert into binning (description) values
("MetaBAT"),
("MaxBin"),
("CONCOCT"),
("Binsanity"),
("MyCC"),
("Cocacola"),
("Anvi'o"),
("Metagenome-Atlas"),
("CheckM"),
("DAS Tool");


insert into sequencing (description) values
("FastQC"),
("Trimmomatic"),
("Cutadapt"),
("SPAdes"),
("MEGAHIT"),
("IDBA-UD"),
("BWA"),
("Bowtie2"),
("HISAT2"),
("GATK"),
("FreeBayes"),
("Samtools"),
("Prokka"),
("InterProScan"),
("EggNOG-mapper"),
("MetaPhlAn"),
("Kraken2"),
("MetaGeneMark");


insert into extraction (description) values
("LabKey"),
("Biotracker"),
("Benchling"),
("OpenLab"),
("LabArchives"),
("Protocols.io"),
("Quartzy"),
("NanoDrop"),
("Qubit"),
("Bioanalyzer"),
("Hamilton Robotics"),
("Tecan");


insert into assembly (description) values
("SPAdes"),
("Velvet"),
("ABySS"),
("Canu"),
("Flye"),
("Shasta"),
("MaSuRCA"),
("HybridSPAdes"),
("MEGAHIT"),
("IDBA-UD"),
("MetaSPAdes"),
("Trinity"),
("Oases"),
("SOAPdenovo"),
("NOVOPlasty"),
("Unicycler");

