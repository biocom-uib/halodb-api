
USE `HaloDB` ;


insert into method(description) values
("BUSCO"),
("CheckM"),
("OrthoDB"),
("Kraken"),
("BlobTools"),
("Anvi’o "),
("MiGA");



insert into oxygen (relationship) values 
("Aerobic metabolism"), 
("Obligate Anaerobic metabolism"), 
("Facultative Anaerobic metabolism"), 
("Microarophiles"), 
("Aerotolerant anaerobes");

insert into temperature (category) values 
("Psychrophyles (-20ºC, 10ºC]"),
("Mesophiles (10ºC, 45ºC]"),
("Moderate thermophiles (45ºC, 60ºC]"),
("Thermophiles (60ºC, 80ºC]"),
("Hyperthermophiles (80ºC, 122ºC)");

insert into ph (category) values 
("Ultra acidic (-∞, 3.5]"),
("Extremely acidic (3.5, 4.5]"),
("Very strongly acidic (4.5, 5.0]"),
("Strongly acidic (5.0, 5.5]"),
("Moderately acidic (5.5, 6.0]"),
("Slightly acidic (6.0, 6.5]"),
("Neutral (6.5, 7.3]"),
("Slightly alkaline (7.3, 7.8]"),
("Moderately alkaline (7.8, 8.4]"),
("Strongly alkaline (8.4, 9.0]"),
("Very strongly alkaline (9.0, 10.5]"),
("Hyper alkaline (10.5, +∞)");

insert into salinity (category) values
("Halotolerants [0%, 1%)"), 
("slight halophiles [1%, 3%)"),
("Moderate halophiles [3%, 15%)"),
("Extreme halophiles [15%, 32%]");

-- ######################################## 
-- insert into salinity (category) values
-- ("Oligohaline [0.5‰, 5‰]"),
-- ("Mesohaline (5‰, 18‰]"),
-- ("Polyhaline (18‰, 30‰]"),
-- ("Euhaline (30‰, 45‰]"),
-- ("Metahaline (45‰, 65‰]"),
-- ("Hyperhaline (65 ‰, +∞)");
-- ########################################

-- ########################################
--  Convertit a enum
-- insert into biosafety (level) values
-- ("BSL-1"),
-- ("BSL-2"),
-- ("BSL-3"),
-- ("BSL-4");
-- ########################################

insert into fraction (name) values
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



insert into target (name) values
("gDNA (genomic DNA)"),
("Exome"),
("mtDNA (mitochondrial DNA)"),
("cpDNA (Chloroplast DNA)"),
("mRNA (Messenger RNA)"),
("tRNA (Transfer RNA)"),
("ncRNA (Non-coding RNA)"),
("RNA (total RNA)");