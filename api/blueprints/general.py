import json
import datetime

from sqlalchemy import func

from flask import jsonify, abort, send_file

from flask import Blueprint
from flask import Response, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from api import log
from api.auth import required_token, verify_token, get_uid_from_request
from api.controllers.GroupController import GroupController

from api.controllers.SampleController import SampleController
from api.controllers.UserController import UserController
from api.db import db
from api.db.models import Sample, Temperature, Ph, Salinity, Experiment, Trimmed_Reads, Contigs, Predicted_Genes, Mags, \
    Contigs_Virus, Genome, Single_Cell, Plasmid
from api.db.db import DatabaseInstance

from api.decorators import wrap_error, get_params, log_params, error, ok_message
from api.field_utils import valid_field, sequences
from api.utils import serialize_datetime
from api.utils import to_dict

from werkzeug.utils import secure_filename

general_page = Blueprint('general_page', __name__)

# limiter = Limiter(get_remote_address)



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
    Return the list of users currently registered in the system
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
@get_params
@log_params
def sequences_list(params: dict, **kwargs):
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

# @general_page.route('/sequence/<string:seq>/', methods=['GET'])
# @wrap_error
# # @limiter.limit("100/minute")
# @get_params
# @log_params
# def sequences_list(params: dict, seq:str, **kwargs):
#     message = ''
#     result_status = 200
#     seq = normalize(seq)
#     if seq not in sequences:
#         error(f"Sequence {seq} not found", 404)
#
#     if request.method == 'GET':
#         log.info('Request received for list of the sequence {seq}')
#         resp = sequences[seq]
#         message = json.dumps(resp, default=serialize_datetime)
#         # message = json.dumps(resp, default=str)
#         result_status = 200
#
#     return Response(response=message,
#                     status=result_status,
#                     mimetype="application/json")

@general_page.route('/query/sequence/<string:name>/', methods=['GET'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
# @required_token
def get_sequence(params: dict, name: str, **kwargs):
    """
    Given a sequence name, return the corresponding sequence steps
    :param params:
    :param name:
    :param kwargs:
    :return:
    """
    log.info('Request to get the genomic sequence related to {name}')

    if name in sequences:
        return jsonify(sequences[name])
    else:
        error(f"Sequence {name} not found", 404)


valid_tables = {'temperature':Temperature, 'ph':Ph, 'salinity':Salinity}

@general_page.route('/query/<string:table>/')
@wrap_error
# @limiter.limit("100/minute")
# @get_params
# @log_params
# @required_token
def get_table_data(table: str):
    """
    Given a classification, return the set of its categories and the corresponding range
    :param table: the classification to be returned
    :return:
    """
    if table not in valid_tables:
        error(f"Table {table} not found", 404)
    else:
        o2 = valid_tables[table].query.all()
        o2_list = to_dict(o2)
        return ok_message(message=o2_list)

        # return Response(response=json.dumps(o2_list),
        #                 status=200,
        #                 mimetype="application/json")


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
    Given a table and a value, return the corresponding category.
    :param table: the categories table where look for the value.
    :param value: the value to be categorized
    :return:
    """
    valid_field("table")
    with DatabaseInstance.get().session() as session:
        if table == 'temperature':
            element = session.query(Temperature).filter(Temperature.vmin < value, value <= Temperature.vmax).first()
            vmin, vmax = session.query(func.min(Temperature.vmin), func.max(Temperature.vmax)).first()
        elif table == 'ph':
            element = session.query(Ph).filter(Ph.vmin < value, value <= Ph.vmax).first()
            vmin, vmax = session.query(func.min(Ph.vmin), func.max(Ph.vmax)).first()
        elif table == 'salinity':
            element = session.query(Salinity).filter(Salinity.vmin < value, value <= Salinity.vmax).first()
            vmin, vmax = session.query(func.min(Salinity.vmin), func.max(Salinity.vmax)).first()
        else:
            element = None
        if element is not None:
            value = element.description
        elif value < vmin:
            value = f"Less than minimum ({vmin})"
        elif value > vmax:
            value = f"More than maximum ({vmax})"
        else:
            value = None
        return jsonify(value)

