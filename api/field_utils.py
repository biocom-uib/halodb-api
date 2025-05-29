import datetime


from api.db.models import Project, Sample, Experiment, Trimmed_Reads, Contigs, Predicted_Genes, Mags, Contigs_Virus, \
    Genome, Single_Cell, Plasmid, Method, Extraction, Assembly, Sequencing, Binning, Oxygen, Fraction, Target, \
    Temperature, Ph, Salinity, Keywords, Publication, Hkgenes, Group_Shared_Experiment, Group_Shared_Trimmed_Reads, \
    Group_Shared_Contigs, Group_Shared_Predicted_Genes, Group_Shared_Mags, Group_Shared_Contigs_Virus, \
    Group_Shared_Genome, Group_Shared_Single_Cell, Group_Shared_Plasmid, User_Shared_Plasmid, User_Shared_Single_Cell, \
    User_Shared_Experiment, User_Shared_Genome, User_Shared_Contigs_Virus, User_Shared_Mags, \
    User_Shared_Predicted_Genes, User_Shared_Contigs, User_Shared_Trimmed_Reads, Group_Shared_Sample, User_Shared_Sample
from api.utils import convert_to_coordinate, commas_to_dot, convert_to_dict

sequences = {
    "METAGENOME": ["RAW READS", "TRIMMED READS", "CONTIGS", "PREDICTED GENES", "MAGS"],
    "METATRANSCRIPTOME": ["RAW READS", "TRIMMED READS"],
    "METAVIROME": ["RAW READS", "TRIMMED READS", "CONTIGS", "PREDICTED GENES", "CONTIGS VIRUS"],
    "GENOME PROCARIOTA": ["RAW READS", "GENOME", "PREDICTED GENES"],
    "GENOME VIRUS": ["RAW READS", "GENOME", "PREDICTED GENES"],
    "PROTEOMICS": ["PEPTIDES"],
    "SINGLE CELL GENOMICS": ["RAW READS", "SINGLE CELL GENOME", "PREDICTED GENES"],
    "PLASMID": ["RAW READS", "PLASMID", "PREDICTED GENES"]
}

# each sequence step has a table associated with it, also it has a parent, depending on the treatment it can be one or
# another, to deal with this, each sequence step has a parent table associated with it.
sequence_step_to_table = {
    "PROJECT": {"table": Project,
                "parent": None
                },
    "SAMPLE": {"table": Sample,
               "parent": {
                   "METAGENOME": "PROJECT",
                   "METATRANSCRIPTOME": "PROJECT",
                   "METAVIROME": "PROJECT",
                   "GENOME PROCARIOTA": "PROJECT",
                   "GENOME VIRUS": "PROJECT",
                   "PROTEOMICS": "PROJECT",
                   "SINGLE CELL GENOMICS": "PROJECT",
                   "PLASMID": "PROJECT"
               },
               "shared_procedure": "get_samples_available"
               },
    "RAW READS": {"table": Experiment,
                  "parent": {
                      "METAGENOME": "SAMPLE",
                      "METATRANSCRIPTOME": "SAMPLE",
                      "METAVIROME": "SAMPLE",
                      "GENOME PROCARIOTA": "SAMPLE",
                      "GENOME VIRUS": "SAMPLE",
                      "PROTEOMICS": None,
                      "SINGLE CELL GENOMICS": "SAMPLE",
                      "PLASMID": "SAMPLE"
                  },
                  "shared_procedure": "get_experiments_available"
                  },
    "TRIMMED READS": {"table": Trimmed_Reads,
                      "parent": {
                          "METAGENOME": "RAW READS",
                          "METATRANSCRIPTOME": "RAW READS",
                          "METAVIROME": "RAW READS",
                          "GENOME PROCARIOTA": None,
                          "GENOME VIRUS": None,
                          "PROTEOMICS": None,
                          "SINGLE CELL GENOMICS": None,
                          "PLASMID": None
                      },
                      "shared_procedure": "get_trimmed_reads_available"
                      },
    "CONTIGS": {"table": Contigs,
                "parent": {
                    "METAGENOME": "TRIMMED READS",
                    "METATRANSCRIPTOME": None,
                    "METAVIROME": "TRIMMED READS",
                    "GENOME PROCARIOTA": None,
                    "GENOME VIRUS": None,
                    "PROTEOMICS": None,
                    "SINGLE CELL GENOMICS": None,
                    "PLASMID": None
                },
                "shared_procedure": "get_contigs_available"
                },
    "PREDICTED GENES": {"table": Predicted_Genes,
                        "parent": {
                            "METAGENOME": "CONTIGS",
                            "METATRANSCRIPTOME": None,
                            "METAVIROME": "CONTIGS",
                            "GENOME PROCARIOTA": "GENOME",
                            "GENOME VIRUS": "GENOME",
                            "PROTEOMICS": None,
                            "SINGLE CELL GENOMICS": "SINGLE CELL GENOME",
                            "PLASMID": "PLASMID"
                        },
                        "shared_procedure": "get_predicted_genes_available"
                        },
    "MAGS": {"table": Mags,
             "parent": {
                 "METAGENOME": "PREDICTED GENES",
                 "METATRANSCRIPTOME": None,
                 "METAVIROME": None,
                 "GENOME PROCARIOTA": None,
                 "GENOME VIRUS": None,
                 "PROTEOMICS": None,
                 "SINGLE CELL GENOMICS": None,
                 "PLASMID": None
             },
             "shared_procedure": "get_mags_available"
             },
    "CONTIGS VIRUS": {"table": Contigs_Virus,
                      "parent": {
                          "METAGENOME": None,
                          "METATRANSCRIPTOME": None,
                          "METAVIROME": "PREDICTED READS",
                          "GENOME PROCARIOTA": None,
                          "GENOME VIRUS": None,
                          "PROTEOMICS": None,
                          "SINGLE CELL GENOMICS": None,
                          "PLASMID": None
                      },
                      "shared_procedure": "get_contigs_virus_available"
                      },
    "GENOME": {"table": Genome,
               "parent": {
                   "METAGENOME": None,
                   "METATRANSCRIPTOME": None,
                   "METAVIROME": None,
                   "GENOME PROCARIOTA": "RAW READS",
                   "GENOME VIRUS": "RAW READS",
                   "PROTEOMICS": None,
                   "SINGLE CELL GENOMICS": None,
                   "PLASMID": None
               },
               "shared_procedure": "get_genomes_available"
               },
    "PEPTIDES": {"table": Experiment,
                 "parent": {
                     "METAGENOME": None,
                     "METATRANSCRIPTOME": None,
                     "METAVIROME": None,
                     "GENOME PROCARIOTA": None,
                     "GENOME VIRUS": None,
                     "PROTEOMICS": "SAMPLE",
                     "SINGLE CELL GENOMICS": None,
                     "PLASMID": None
                 },
                 "shared_procedure": "get_experiments_available"
                 },
    "SINGLE CELL GENOME": {"table": Single_Cell,
                           "parent": {
                               "METAGENOME": None,
                               "METATRANSCRIPTOME": None,
                               "METAVIROME": None,
                               "GENOME PROCARIOTA": None,
                               "GENOME VIRUS": None,
                               "PROTEOMICS": None,
                               "SINGLE CELL GENOMICS": "RAW READS",
                               "PLASMID": None
                           },
                           "shared_procedure": "get_single_cells_available"
                           },
    "PLASMID": {"table": Plasmid,
                "parent": {
                    "METAGENOME": None,
                    "METATRANSCRIPTOME": None,
                    "METAVIROME": None,
                    "GENOME PROCARIOTA": None,
                    "GENOME VIRUS": None,
                    "PROTEOMICS": None,
                    "SINGLE CELL GENOMICS": None,
                    "PLASMID": "RAW READS"
                },
                "shared_procedure": "get_plasmids_available"
                }
}

# The shared tables are the tables that are shared between users and groups. The shared tables are the tables that
# have a user_id and a group_id, and also the access mode allowed to the user or group, that can be 'read' or 'readwrite'.
sequence_step_sharings = {
    "SAMPLE": {"group": Group_Shared_Sample, "user": User_Shared_Sample},
    "RAW READS": {"group": Group_Shared_Experiment, "user": User_Shared_Experiment},
    "TRIMMED READS": {"group": Group_Shared_Trimmed_Reads, "user": User_Shared_Trimmed_Reads},
    "CONTIGS": {"group": Group_Shared_Contigs, "user": User_Shared_Contigs},
    "PREDICTED GENES": {"group": Group_Shared_Predicted_Genes, "user": User_Shared_Predicted_Genes},
    "MAGS": {"group": Group_Shared_Mags, "user": User_Shared_Mags},
    "CONTIGS VIRUS": {"group": Group_Shared_Contigs_Virus, "user": User_Shared_Contigs_Virus},
    "GENOME": {"group": Group_Shared_Genome, "user": User_Shared_Genome},
    "PEPTIDES": {"group": Group_Shared_Experiment, "user": User_Shared_Experiment},
    "SINGLE CELL GENOMICS": {"group": Group_Shared_Single_Cell, "user": User_Shared_Single_Cell},
    "PLASMID": {"group": Group_Shared_Plasmid, "user": User_Shared_Plasmid}
}

excluded_fields = {
    "METAGENOME": {
        "RAW READS": [],
        "TRIMMED READS": [],
        "CONTIGS": [],
        "PREDICTED GENES": [],
        "MAGS": []
    },
    "METATRANSCRIPTOME": {
        "RAW READS": ["gsiz", "sfrac"],
        "TRIMMED READS": ["coverage"]
    },
    "METAVIROME": {
        "RAW READS": ["gsiz", "sfrac"],
        "TRIMMED READS": [],
        "CONTIGS": [],
        "PREDICTED GENES": [],
        "CONTIGS VIRUS": []
    },
    "GENOME PROCARIOTA": {
        "RAW READS": ["meca", "gsiz", "sfrac"],
        "GENOME": [],

        "PREDICTED GENES": []
    },
    "GENOME VIRUS": {
        "RAW READS": ["meca", "gsiz", "sfrac"],
        "GENOME": ["txnr", "sixteensr", "seqdepth", "twentythreesr", "dnae", "tems", "phsa", "sals", "emet", "orel",
                   "elac", "temo", "teml", "temh", "phop", "phlo", "phhi", "salo", "sall", "salh", "salw", "path",
                   "extr"],
        "PREDICTED GENES": []
    },
    "PROTEOMICS": {
        "PEPTIDES": ["meca", "gsiz", "seqt", "dati", "sfrac"]
    },
    "SINGLE CELL GENOMICS": {
        "RAW READS": ["meca", "gsiz", "sfrac"],
        "SINGLE CELL GENOME": [],
        "PREDICTED GENES": []
    },
    "PLASMID": {
        "RAW READS": ["gsiz", "sfrac"],
        "PLASMID": [],
        "PREDICTED GENES": []
    }
}

file_fields = {
    "rreads": {"name": "rrname", "steps": ["RAW READS", "PEPTIDES"]},
    "rreads2": {"name": "rrname2", "steps": ["RAW READS", "PEPTIDES"]},
    "treads": {"name": "trname", "steps": ["TRIMMED READS"]},
    "assembled": {"name": "assname", "steps": ["CONTIGS", "GENOME", "SINGLE CELL GENOME", "PLASMID"]},
    "pgenes": {"name": "pgenesname", "steps": ["PREDICTED GENES"]},
}

file_fields_names = { "rrname", "rrname2", "trname", "assname", "pgenesname"}

forbidden_files = [
    "created", "updated", "id", "is_public", "source_id", "project_id", "user_id"
]

date_fields = ["dats", "dati"]
time_fields = ["hocs"]

coord_fields = ["lati", "long"]
float_fields = ["ssize", "seqdepth", "completeness", "contamination", "ggcm", "alti", "dept", "tems", "phsa", "sals",
                "temo", "teml", "temh", "phop", "phlo", "phhi", "salo", "sall", "salh", "coverage"]

complementaries = {
    "method_id": Method,
    "dnae": Extraction,
    "asem": Assembly,
    "seqt": Sequencing,
    "bins": Binning,
    "orel": Oxygen,
    "sfrac": Fraction,
    "target_id": Target
}

supplementaries = {
    "temc": {"field": "temo", "table": Temperature},
    "phca": {"field": "phop", "table": Ph},
    "salc": {"field": "salo", "table": Salinity}
}

multi_complementaries = {
    "keywords_id": "Keywords",
    "publication_id": "Publication",
    "hkgn": "Hkgenes"
}

extra_headers = ['public', 'owned', 'shared_by_group', 'shared_by_others', 'access_mode',
                 'group_relation', 'group_id', 'group_name']
extra_values = [1, 0, 0, 0, 'read', None, None, None]


def merge_extra_fields(element):
    """
    Merge the extra fields to an element such a sample or an omic sequence step
    :param element:
    :return:
    """
    keys = list(element.keys())
    values = list(element.values())
    merged_keys = extra_headers + keys
    merged_values = extra_values + values
    return convert_to_dict(merged_values, merged_keys)


def get_stored_procedure(step: str):
    return sequence_step_to_table[step]['shared_procedure']


def is_valid_sequence(sequence: str) -> bool:
    """
    Test if a sequence is valid, that means it's a key in the sequences dictionary.
    The matching has to be exact.
    :param sequence:
    :return:
    """
    # This can match any key that partially contains the given sequence.
    # return sequence in sequences.keys()
    found = False
    for key in sequences.keys():
        if sequence == key:
            found = True
            break
    return found


def filter_coordinates(fields: dict) -> dict:
    """
    Filter the coordinates from a dictionary. The coordinates are the fields lati and long.
    :param fields: the dictionary to be filtered
    :return: the dictionary with the coordinates removed
    """
    duplicate = fields.copy()
    for fld in coord_fields:
        if fld in fields.keys():
            duplicate[fld] = convert_to_coordinate(fields[fld])
    return duplicate


def filter_floats(fields: dict) -> dict:
    duplicate = fields.copy()
    for fld in float_fields:
        if fld in fields.keys():
            duplicate[fld] = commas_to_dot(fields[fld])
    return duplicate


def is_valid_step(step: str) -> bool:
    """
    Test if a step is valid, that means it's a key in the sequence_step_to_table dictionary. The matching has to be exact.
    :param step:
    :return:
    """
    # This can match any key that partially contains the given sequence.
    # return sequence in sequences.keys()
    found = False
    for key in sequence_step_to_table.keys():
        if step == key:
            found = True
            break
    return found


def are_valid_sequence_step(sequence: str, step: str) -> bool:
    """
    Test if a step is valid for a given sequence. That means the step has to be a key in the list of steps for the given
    sequence. The matching has to be exact.
    :param sequence: The omic sequence to take into account
    :param step: The step to test if it's valid
    :return:
    """
    found = False
    for key in sequences[sequence]:
        if step == key:
            found = True
            break
    return found


def fix_times(data: dict):
    """
    This method fixes the content of the strictly date and time fields. The date fields are fixed to the format dd/mm/yyyy
    and the time fields to the format hh:mm:ss.
    :param data:
    :return:
    """
    for key in date_fields:
        if key in data.keys():
            data[key] = datetime.datetime.strptime(data[key], '%d/%m/%Y')
    for key in time_fields:
        if key in data.keys():
            len_time = len(data[key].split(":"))
            if len_time < 2:
                data[key] = datetime.datetime.strptime(data[key], '%H')
            if len_time < 3:
                data[key] = datetime.datetime.strptime(data[key], '%H:%M')
            else:
                data[key] = datetime.datetime.strptime(data[key], '%H:%M:%S')


def is_file_field(field):
    """
    Check if a field is a valid file field
    :param field: the field to check if it's a file field
    :return: true if field is a file field, false otherwise
    """
    return field in file_fields.keys()

def get_file_name_field_raw(field):
    """
    Get the name of the field that stores the actual file name for a given field
    :param field:
    :return:
    """
    if is_file_field(field):
        return file_fields[field]['name']
    return None

def get_file_name_field(step, field):
    """
    Get the name of the field that stores the actual file name for a given field with the restriction of the step, that
    is, the field has to be a file field and the step has to be in the list of valid steps for the field.
    :param step:
    :param field:
    :return:
    """
    if is_file_field(field) and step in file_fields[field]['steps']:
        return file_fields[field]['name']
    return None


def exclude_param_files(params: dict):
    """
    Given a list of parameters, remove the params that are related to files.
    :param params: the list of params to filter.
    :return: the params received, but excluding those related to files.
    """
    return {k: v for k, v in params.items()
            if k not in file_fields.keys() and k not in file_fields_names}
            # if k not in file_fields.keys() and k not in file_fields.values()['name']}


def exclude_forbidden_fields(params: dict, sequence: str = None, step: str = None):
    """
    Remove the list of parameters that are forbidden for a given sequence and step into the sequence.
     That is the fields that are acceptable for a given treatment and sequence are returned.
     Each field that is not acceptable is removed.
    :param sequence: the omic sequence to be considered
    :param step: the step into the omic sequence to be used
    :param params: the list of parameters to be filtered
    :return:
    """

    def filter_fields(fields, excluded):
        return {k: v for k, v in fields.items() if k not in excluded}

    params = filter_fields(params, forbidden_files)
    if step is not None and sequence is not None:
        selected = excluded_fields[sequence][step]
        params = filter_fields(params, selected)
    return params


def valid_field(field):
    """
    Check if a field is a valid field. That is, it's neither a file field nor a forbidden field.
            The field is valid, but it has to be treated in a special way.
    :param field:
    :return:
    """
    # This doesn't work because the field "name" fails against "rrname", "tsname", ...
    #
    # return (field not in cls.__file_fields__.keys() and
    #        field not in cls.__file_fields__.values() and
    #        field not in cls.__forbidden_files__)

    is_valid = True
    for key in file_fields.keys():
        if key == field:
            is_valid = False
            break
    if is_valid:
        for value in file_fields_names:
            if value == field:
                is_valid = False
                break
        if is_valid:
            for forbidden in forbidden_files:
                if forbidden == field:
                    is_valid = False
                    break
    return is_valid


not_to_return = ["user", "group",
                 "password",
                 "author", "project", "user_has_group",
                 "sample", "experiment", "trimmed_reads", "contigs", "predicted_genes", "mags",
                 "contigs_virus", "genome", "single_cell", "plasmid",
                 "user_shared_sample", "group_shared_sample",
                 "user_shared_experiment", "group_shared_experiment",
                 "user_shared_trimmed_reads", "group_shared_trimmed_reads",
                 "user_shared_contigs", "group_shared_contigs",
                 "user_shared_predicted_genes", "group_shared_predicted_genes",
                 "user_shared_mags", "group_shared_mags",
                 "user_shared_contigs_virus", "group_shared_contigs_virus",
                 "user_shared_genome", "group_shared_genome",
                 "user_shared_single_cell", "group_shared_single_cell",
                 "user_shared_plasmid", "group_shared_plasmid"]


def filter_dict(data: dict):
    """
    Extract the keys from a dictionary
    :param data: the dictionary to extract the keys from
    :return: a dictionary with the extracted keys
    """
    return {k: v for k, v in data.items() if k not in not_to_return}


def get_reference_tables(sequence_name: str, step_name: str):
    """
    Get the tables that are related to a sequence
    :param sequence_name:
    :param step_name:
    :return: the pair table-parent table corresponding to the sequence, or None if the sequence is not found
    """
    if sequence_name in sequences:
        if step_name in sequence_step_to_table:
            actual = sequence_step_to_table[step_name]['table']
            parentname = sequence_step_to_table[step_name]['parent'][sequence_name]
            parent = sequence_step_to_table[parentname]['table'] if parentname is not None else None
            return actual, parent
        else:
            return None, None
    else:
        return None, None


def get_step_table(step: str):
    """
    Get the table associated with a step
    :param step:
    :return:
    """
    step = step.upper()
    if step in sequence_step_to_table:
        return sequence_step_to_table[step]['table']
    else:
        return None


def get_sharing_tables(sequence_step: str):
    """
    Get the sharing tables associated with a sequence step.
    :param sequence_step:
    :return:
    """
    sequence_step = sequence_step.upper()
    if sequence_step in sequence_step_sharings:
        return sequence_step_sharings[sequence_step]
    else:
        return None
