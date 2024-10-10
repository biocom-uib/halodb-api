USE `halodb`;
-- ----------------------------------------------------
--  samples
-- ----------------------------------------------------
DROP procedure IF EXISTS `get_samples_available`;

DELIMITER $$
USE `halodb`$$
CREATE PROCEDURE `get_samples_available`(IN userId INT)
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
			JOIN `halodb`.`group_shared_sample` AS gs ON ug.group_id = gs.group_id
			JOIN `halodb`.`sample` AS s ON gs.shared_id = s.id
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
			JOIN user_shared_sample uss ON s.id = uss.shared_id
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

-- ----------------------------------------------------
--  experiments
-- ----------------------------------------------------
DROP procedure IF EXISTS `get_experiments_available`;

DELIMITER $$
USE `halodb`$$
CREATE PROCEDURE `get_experiments_available`(IN userId INT)
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
	FROM experiment AS s
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
	FROM experiment AS s
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
			JOIN `halodb`.`group_shared_experiment` AS gs ON ug.group_id = gs.group_id
			JOIN `halodb`.`experiment` AS s ON gs.shared_id = s.id
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
		FROM experiment s
			JOIN user_shared_experiment uss ON s.id = uss.shared_id
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
    experiment.*
    FROM relations
    JOIN experiment ON experiment.id = relations.id
    ORDER BY id;
END$$

DELIMITER ;

-- ----------------------------------------------------
--  trimmed_reads
-- ----------------------------------------------------
DROP procedure IF EXISTS `get_trimmed_reads_available`;

DELIMITER $$
USE `halodb`$$
CREATE PROCEDURE `get_trimmed_reads_available`(IN userId INT)
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
	FROM trimmed_reads AS s
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
	FROM trimmed_reads AS s
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
			JOIN `halodb`.`group_shared_trimmed_reads` AS gs ON ug.group_id = gs.group_id
			JOIN `halodb`.`trimmed_reads` AS s ON gs.shared_id = s.id
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
		FROM trimmed_reads s
			JOIN user_shared_trimmed_reads uss ON s.id = uss.shared_id
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
    trimmed_reads.*
    FROM relations
    JOIN trimmed_reads ON trimmed_reads.id = relations.id
    ORDER BY id;
END$$

DELIMITER ;

-- ----------------------------------------------------
--  contigs
-- ----------------------------------------------------
DROP procedure IF EXISTS `get_contigs_available`;

DELIMITER $$
USE `halodb`$$
CREATE PROCEDURE `get_contigs_available`(IN userId INT)
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
	FROM contigs AS s
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
	FROM contigs AS s
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
			JOIN `halodb`.`group_shared_contigs` AS gs ON ug.group_id = gs.group_id
			JOIN `halodb`.`contigs` AS s ON gs.shared_id = s.id
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
		FROM contigs s
			JOIN user_shared_contigs uss ON s.id = uss.shared_id
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
    contigs.*
    FROM relations
    JOIN contigs ON contigs.id = relations.id
    ORDER BY id;
END$$

DELIMITER ;

-- ----------------------------------------------------
--  predicted_genes
-- ----------------------------------------------------
DROP procedure IF EXISTS `get_predicted_genes_available`;

DELIMITER $$
USE `halodb`$$
CREATE PROCEDURE `get_predicted_genes_available`(IN userId INT)
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
	FROM predicted_genes AS s
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
	FROM predicted_genes AS s
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
			JOIN `halodb`.`group_shared_predicted_genes` AS gs ON ug.group_id = gs.group_id
			JOIN `halodb`.`predicted_genes` AS s ON gs.shared_id = s.id
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
		FROM predicted_genes s
			JOIN user_shared_predicted_genes uss ON s.id = uss.shared_id
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
    predicted_genes.*
    FROM relations
    JOIN predicted_genes ON predicted_genes.id = relations.id
    ORDER BY id;
END$$

DELIMITER ;

-- ----------------------------------------------------
--  mags
-- ----------------------------------------------------
DROP procedure IF EXISTS `get_mags_available`;

DELIMITER $$
USE `halodb`$$
CREATE PROCEDURE `get_mags_available`(IN userId INT)
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
	FROM mags AS s
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
	FROM mags AS s
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
			JOIN `halodb`.`group_shared_mags` AS gs ON ug.group_id = gs.group_id
			JOIN `halodb`.`mags` AS s ON gs.shared_id = s.id
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
		FROM mags s
			JOIN user_shared_mags uss ON s.id = uss.shared_id
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
    mags.*
    FROM relations
    JOIN mags ON mags.id = relations.id
    ORDER BY id;
END$$

DELIMITER ;

-- ----------------------------------------------------
--  contigs_virus
-- ----------------------------------------------------
DROP procedure IF EXISTS `get_contigs_virus_available`;

DELIMITER $$
USE `halodb`$$
CREATE PROCEDURE `get_contigs_virus_available`(IN userId INT)
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
	FROM contigs_virus AS s
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
	FROM contigs_virus AS s
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
			JOIN `halodb`.`group_shared_contigs_virus` AS gs ON ug.group_id = gs.group_id
			JOIN `halodb`.`contigs_virus` AS s ON gs.shared_id = s.id
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
		FROM contigs_virus s
			JOIN user_shared_contigs_virus uss ON s.id = uss.shared_id
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
    contigs_virus.*
    FROM relations
    JOIN contigs_virus ON contigs_virus.id = relations.id
    ORDER BY id;
END$$

DELIMITER ;

-- ----------------------------------------------------
--  genome
-- ----------------------------------------------------
DROP procedure IF EXISTS `get_genomes_available`;

DELIMITER $$
USE `halodb`$$
CREATE PROCEDURE `get_genomes_available`(IN userId INT)
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
	FROM genome AS s
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
	FROM genome AS s
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
			JOIN `halodb`.`group_shared_genome` AS gs ON ug.group_id = gs.group_id
			JOIN `halodb`.`genome` AS s ON gs.shared_id = s.id
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
		FROM genome s
			JOIN user_shared_genome uss ON s.id = uss.shared_id
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
    genome.*
    FROM relations
    JOIN genome ON genome.id = relations.id
    ORDER BY id;
END$$

DELIMITER ;

-- ----------------------------------------------------
--  single_cell
-- ----------------------------------------------------
DROP procedure IF EXISTS `get_single_cells_available`;

DELIMITER $$
USE `halodb`$$
CREATE PROCEDURE `get_single_cells_available`(IN userId INT)
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
	FROM single_cell AS s
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
	FROM single_cell AS s
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
			JOIN `halodb`.`group_shared_single_cell` AS gs ON ug.group_id = gs.group_id
			JOIN `halodb`.`single_cell` AS s ON gs.shared_id = s.id
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
		FROM single_cell s
			JOIN user_shared_single_cell uss ON s.id = uss.shared_id
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
    single_cell.*
    FROM relations
    JOIN single_cell ON single_cell.id = relations.id
    ORDER BY id;
END$$

DELIMITER ;

-- ----------------------------------------------------
--  plasmid
-- ----------------------------------------------------
DROP procedure IF EXISTS `get_plasmids_available`;

DELIMITER $$
USE `halodb`$$
CREATE PROCEDURE `get_plasmids_available`(IN userId INT)
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
	FROM plasmid AS s
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
	FROM plasmid AS s
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
			JOIN `halodb`.`group_shared_plasmid` AS gs ON ug.group_id = gs.group_id
			JOIN `halodb`.`plasmid` AS s ON gs.shared_id = s.id
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
		FROM plasmid s
			JOIN user_shared_plasmid uss ON s.id = uss.shared_id
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
    plasmid.*
    FROM relations
    JOIN plasmid ON plasmid.id = relations.id
    ORDER BY id;
END$$

DELIMITER ;

