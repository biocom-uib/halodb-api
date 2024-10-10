from api.db import db
from api.db.db import DatabaseInstance, Base
from api.utils import from_dict, as_dict

if DatabaseInstance.get() is None:
    raise RuntimeError('The database has not been initialized yet, this module should be imported later')

Assembly = Base.classes.assembly
Author = Base.classes.author
Binning = Base.classes.binning
Contigs = Base.classes.contigs
Contigs_Virus = Base.classes.contigs_virus
Experiment = Base.classes.experiment
Extraction = Base.classes.extraction
Fraction = Base.classes.fraction
Genome = Base.classes.genome
Group = Base.classes.group
Hkgenes = Base.classes.hkgenes
Keywords = Base.classes.keywords
Mags = Base.classes.mags
Method = Base.classes.method
Oxygen = Base.classes.oxygen
Ph = Base.classes.ph
Plasmid = Base.classes.plasmid
Predicted_Genes = Base.classes.predicted_genes
Project = Base.classes.project
Publication = Base.classes.publication
Salinity = Base.classes.salinity
Sample = Base.classes.sample
Sequencing = Base.classes.sequencing
Single_Cell = Base.classes.single_cell
Target = Base.classes.target
Temperature = Base.classes.temperature
Trimmed_Reads = Base.classes.trimmed_reads
User = Base.classes.user

# ## Additional associative tables, with some attributes

User_Has_Group = Base.classes.user_has_group

# user_project is an associative relation. It does not have any additional attributes, so it is not necessary to create a class for it.
# User_Project = Base.classes.user_project

Publication_Has_Author = Base.classes.publication_has_author

# sample_has_keywords is an associative relation. It does not have any additional attributes, so it is not necessary to create a class for it.
# Sample_Has_Keywords = Base.classes.sample_has_keywords

# The housekeeping shared relations are associative relations. They do not have any additional attributes, so it is not necessary to create a class for them.
# Housekeeping_Shared_Genome = Base.classes.housekeeping_shared_genome
# Housekeeping_Shared_Mags = Base.classes.housekeeping_shared_mags
# Housekeeping_Shared_Plasmid = Base.classes.housekeeping_shared_plasmid
# Housekeeping_Shared_Single_Cell = Base.classes.housekeeping_shared_single_cell

Group_Shared_Contigs = Base.classes.group_shared_contigs
Group_Shared_Contigs_Virus = Base.classes.group_shared_contigs_virus
Group_Shared_Experiment = Base.classes.group_shared_experiment
Group_Shared_Genome = Base.classes.group_shared_genome
Group_Shared_Mags = Base.classes.group_shared_mags
Group_Shared_Plasmid = Base.classes.group_shared_plasmid
Group_Shared_Predicted_Genes = Base.classes.group_shared_predicted_genes
Group_Shared_Sample = Base.classes.group_shared_sample
Group_Shared_Single_Cell = Base.classes.group_shared_single_cell
Group_Shared_Trimmed_Reads = Base.classes.group_shared_trimmed_reads

User_Shared_Contigs = Base.classes.user_shared_contigs
User_Shared_Contigs_Virus = Base.classes.user_shared_contigs_virus
User_Shared_Experiment = Base.classes.user_shared_experiment
User_Shared_Genome = Base.classes.user_shared_genome
User_Shared_Mags = Base.classes.user_shared_mags
User_Shared_Plasmid = Base.classes.user_shared_plasmid
User_Shared_Predicted_Genes = Base.classes.user_shared_predicted_genes
User_Shared_Sample = Base.classes.user_shared_sample
User_Shared_Single_Cell = Base.classes.user_shared_single_cell
User_Shared_Trimmed_Reads = Base.classes.user_shared_trimmed_reads


class_list = [
    Assembly,
    Author,
    Binning,
    Contigs,
    Contigs_Virus,
    Experiment,
    Extraction,
    Fraction,
    Genome,
    Group,
    Hkgenes,
    Keywords,
    Mags,
    Method,
    Oxygen,
    Ph,
    Plasmid,
    Predicted_Genes,
    Project,
    Publication,
    Salinity,
    Sample,
    Sequencing,
    Single_Cell,
    Target,
    Temperature,
    Trimmed_Reads,
    User,

    # Housekeeping_Shared_Genome,
    # Housekeeping_Shared_Mags,
    # Housekeeping_Shared_Plasmid,
    # Housekeeping_Shared_Single_Cell,

    Publication_Has_Author,

    User_Has_Group,
    # User_Project,

    # Sample_Has_Keywords,

    Group_Shared_Contigs,
    Group_Shared_Contigs_Virus,
    Group_Shared_Experiment,
    Group_Shared_Genome,
    Group_Shared_Mags,
    Group_Shared_Plasmid,
    Group_Shared_Predicted_Genes,
    Group_Shared_Sample,
    Group_Shared_Single_Cell,
    Group_Shared_Trimmed_Reads,

    User_Shared_Contigs,
    User_Shared_Contigs_Virus,
    User_Shared_Experiment,
    User_Shared_Genome,
    User_Shared_Mags,
    User_Shared_Plasmid,
    User_Shared_Predicted_Genes,
    User_Shared_Sample,
    User_Shared_Single_Cell,
    User_Shared_Trimmed_Reads

]

for c in class_list:
    c.as_dict = as_dict
    c.from_dict = from_dict
