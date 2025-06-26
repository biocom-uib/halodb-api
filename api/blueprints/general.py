import json

from flask import Blueprint
from flask import Response, request
from flask import jsonify
from sqlalchemy import func

from api import log
from api.controllers.GroupController import GroupController
from api.controllers.UserController import UserController
from api.db.models import Temperature, Ph, Salinity, Target, Method, Extraction, Assembly, Sequencing, Binning, Oxygen, \
    Fraction, Keywords, Dois, Hkgenes
from api.decorators import wrap_error, get_params, log_params, error, ok_message
from api.field_utils import sequences, multi_complementaries
from api.utils import serialize_datetime, normalize
from api.utils import to_dict

general_page = Blueprint('general_page', __name__)




# ##############################################################
# General handling
# ##############################################################

@general_page.route('/users/', methods=['GET'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
def users(params: dict, **kwargs):
    """
    Returns the list of users currently registered in the system.
    TODO: This method should be protected and only available for admin users. Or also the information should be
    restricted to the user itself. Or the provided information should be restricted (no password, no email, etc.)

    :param params:
    :param kwargs:
    :return:
    """
    message = ''
    result_status = 200

    if request.method == 'GET':
        log.info('Request received for list of users')
        resp = UserController.list_users()
        message = json.dumps(resp, default=serialize_datetime)
        # message = json.dumps(resp, default=str)
        result_status = 200

    return Response(response=message,
                    status=result_status,
                    mimetype="application/json")


@general_page.route('/groups/', methods=['GET'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
def groups(params: dict, **kwargs):
    """
    Returns the list of groups currently defined in the system.
    :param params:
    :param kwargs:
    :return:
    """
    message = ''
    result_status = 200

    if request.method == 'GET':
        log.info('Request received for list of groups')
        resp = GroupController.list_groups()
        message = json.dumps(resp, default=serialize_datetime)
        # message = json.dumps(resp, default=str)
        result_status = 200

    return Response(response=message,
                    status=result_status,
                    mimetype="application/json")


@general_page.route('/sequences/', methods=['GET'])
@wrap_error
# @limiter.limit("100/minute")
# @get_params
# @log_params
def sequences_list():
    """
    Returns the structure of the omic sequences defined. By now, the sequences are hardcoded and are the following

    - METAGENOME: RAW READS, TRIMMED READS, CONTIGS, PREDICTED GENES, MAGS
    - METATRANSCRIPTOME: RAW READS, TRIMMED READS
    - METAVIROME: RAW READS, TRIMMED READS, CONTIGS, PREDICTED GENES, CONTIGS VIRUS
    - GENOME PROCARIOTA: RAW READS, GENOME, PREDICTED GENES
    - GENOME VIRUS: RAW READS, GENOME, PREDICTED GENES
    - PROTEOMICS: PEPTIDES
    - SINGLE CELL GENOMICS: RAW READS, SINGLE CELL GENOME, PREDICTED GENES
    - PLASMID: RAW READS, PLASMID, PREDICTED GENES

    :return:
    """
    message = ''
    result_status = 200

    if request.method == 'GET':
        log.info('Request received for list of the sequences')
        resp = sequences
        message = json.dumps(resp, default=serialize_datetime)
        # message = json.dumps(resp, default=str)
        result_status = 200

    return Response(response=message,
                    status=result_status,
                    mimetype="application/json")



@general_page.route('/query/sequence/<string:name>/', methods=['GET'])
@wrap_error
# @limiter.limit("100/minute")
# @get_params
# @log_params
# @required_token
def get_sequence(name: str): # , **kwargs
    """
    Given an omic sequence name, return the corresponding omic sequence steps
    :param name: the name of the omic sequence
    :return: the list of valid steps for the omic sequence
    """
    name = normalize(name)

    log.info('Request to get the omic sequence related to {name}')

    if name in sequences:
        return jsonify(sequences[name])
    else:
        error(f"Sequence {name} not found", 404)


valid_tables = {'temperature':Temperature, 'ph':Ph, 'salinity':Salinity}
complementary_valid_tables = {
    "method": Method,
    "dna": Extraction,
    "assembly": Assembly,
    "sequencing": Sequencing,
    "binning": Binning,
    "oxygen": Oxygen,
    "fraction": Fraction,
    "target": Target
}

@general_page.route('/query/<string:table>/')
@wrap_error
# @limiter.limit("100/minute")
# @get_params
# @log_params
# @required_token
def get_table_data(table: str):
    """
    Returns the set of its categories and the corresponding range for a given classification.
    The possible classifications are: temperature, ph, salinity.

    :param table: the classification to be returned
    :return:
    """
    table = table.lower()

    if table not in valid_tables and table not in complementary_valid_tables and table not in multi_complementaries:
        error(f"Table {table} not found", 404)
        return None
    else:
        if table in valid_tables:
            o2 = valid_tables[table].query.all()
        elif table in multi_complementaries:
            o2 = multi_complementaries[table].query.all()
        else:
            o2 = complementary_valid_tables[table].query.all()

        o2_list = to_dict(o2)
        return ok_message(message=o2_list)


# ##############################################################
# Category handling
# ##############################################################
@general_page.route('/query/<string:table>/<float:value>/', methods=['GET'])
@wrap_error
# @limiter.limit("100/minute")
# @get_params
# @log_params
# @required_token
def get_classification_data(table: str, value: float):
    """
    Given a classification and a value, returns the range corresponding to the value.
    :param table: the categories table where look for the value.
    :param value: the value to be categorized
    :return:
    """

    table = table.lower()

    if table not in valid_tables:
        error(f"Table {table} not found", 404)
    else:
        dbtable = valid_tables[table]
        element = dbtable.query.filter(dbtable.vmin < value, value <= dbtable.vmax).first()

        if element is not None:
            value = element.description
        else:
            vmin, vmax = dbtable.query.with_entities(func.min(dbtable.vmin), func.max(dbtable.vmax)).first()
            if value <= vmin:
                value = f"Less than minimum ({vmin})"
            else: # value > vmax
                value = f"More than maximum ({vmax})"

        return jsonify(value)

