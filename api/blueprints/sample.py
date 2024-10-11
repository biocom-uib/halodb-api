import json
import datetime

from flask import jsonify, abort, send_file

from flask import Blueprint
from flask import Response, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from api import log
from api.auth import required_token, verify_token, get_uid_from_request
from api.controllers.ProjectController import ProjectController

from api.controllers.SampleController import SampleController
from api.controllers.UserController import UserController
from api.db import db
from api.db.models import Sample, Temperature, Ph, Salinity
from api.db.db import DatabaseInstance
from api.decorators import wrap_error, get_params, log_params
from api.field_utils import exclude_param_files, exclude_forbidden_fields, valid_field, is_valid_sequence, \
    is_valid_step, get_reference_tables, filter_coordinates, filter_floats
from api.utils import serialize_datetime, convert_to_coordinate, commas_to_dot, normalize
from api.utils import to_dict

from werkzeug.utils import secure_filename

sample_page = Blueprint('sample_page', __name__)

# limiter = Limiter(get_remote_address)


# ##############################################################
# Sample handling
# ##############################################################

@sample_page.route('/sample/', methods=['POST'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def upload_sample(params: dict, **kwargs):
    log.info('Request received for uploading a sample')
    uid: str = kwargs['uid']
    user = UserController.get_user_by_uid(uid)

    if "project_id" in params:
        project_id = params['project_id']
        if len(project_id) == 0:
            project_id = None
    else:
        project_id = None

    # The fields related to the files are treated in a special way.
    # Then, they are not included in the creation of the sample.
    params = exclude_param_files(params)
    params = exclude_forbidden_fields(params, None, None)

    invalid = [fld for fld in params if not valid_field(fld)]
    if len(invalid) == 0:
        try:
            # if a project has been provided, put its id in the sample
            if project_id is not None:
                params['project_id'] = project_id

            # the creation and update dates are the same, the sample is new.
            now = datetime.datetime.now()
            params['created'] = now
            params['updated'] = now

            # A new sample is not public.
            params['is_public'] = False

            # The coordinates are provided as strings, convert them to float
            params = filter_coordinates(params)
            # The floats are provided with commas, convert them to dots
            params = filter_floats(params)

            sample_created = SampleController.create_sample(params, user.id)  # user['id'])
            # sample_created = SampleController.create_sequence_step(params, None, "SAMPLE", user.id)

            message = {'status': 'success',
                       'message': 'Sample created',
                       'sample': SampleController.filter_description_fields(sample_created)
                       }
            result_status = 200
        except Exception as e:
            message = {'status': 'error',
                       'message': str(e)
                       }
            result_status = 400
    else:
        message = {'status': 'error',
                   'message': 'wrong field names',
                   'fields': invalid}
        result_status = 400

    return Response(response=json.dumps(message, default=str),
                    status=result_status,
                    mimetype="application/json")


def get_user_and_sample_id_by_uuid(uid, id_sample):
    """
    Given a user uid and a sample id, return the user id and the sample.
    if the sample can be accessed by the user.

    :param uid: the uid of the user
    :param id_sample: the id of the sample
    :return:
    """
    user = UserController.get_user_by_uid(uid)
    if user is None:
        abort(400, f'User with uid {uid} not found')
    else:
        user_id = user.id

    sample: Sample = SampleController.get_sample_by_id(id_sample)

    if sample is None:
        abort(400, f'Sample with id {id_sample} not found')

    if SampleController.get_access_mode(user_id, id_sample) is None:
        abort(403, f"User {user_id} doesn't have access to sample {id_sample}")

    return user_id, sample


@sample_page.route('/sample/<int:id_sample>/', methods=['PUT', 'PATCH'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def update_fields_sample(params: dict, id_sample: int, **kwargs):
    log.info('Request received for update a sample')
    uid: str = kwargs['uid']

    user_id, sample = get_user_and_sample_id_by_uuid(uid, id_sample)

    access = SampleController.get_access_mode(user_id, id_sample)
    if access is None or access != 'readwrite':
        abort(403, f"User {user_id} doesn't have the privileges to modify the sample {id_sample}")

    # The fields related to the files are treated in a special way.
    # Then, they are not included in the creation of the sample.
    params = exclude_param_files(params)
    params = exclude_forbidden_fields(params)

    invalid = [fld for fld in params if not valid_field(fld)]
    if len(invalid) == 0:
        try:
            sample_updated = SampleController.update_sample(id_sample, params)
            message = {'status': 'success',
                       'message': 'Sample created',
                       'sample': SampleController.filter_description_fields(sample_updated)
                       }
            result_status = 200
        except Exception as e:
            message = {'status': 'error',
                       'message': str(e)
                       }
            result_status = 400
    else:
        message = {'status': 'error',
                   'message': 'wrong field names',
                   'fields': invalid}
        result_status = 400

    return Response(response=json.dumps(message, default=str),
                    status=result_status,
                    mimetype="application/json")


@sample_page.route('/sample/<int:id_sample>/', methods=['GET'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
# @required_token
def get_sample(params: dict, id_sample: int, **kwargs):
    # uid: str = kwargs['uid']
    uid = get_uid_from_request(False)

    if uid is None:
        log.info(f'Request received to get {id_sample =} as public sample')
        sample = SampleController.get_sample_by_id(id_sample)

        if sample is None:
            abort(400, f'Sample with id {id_sample} not found')

        if not sample.is_public:
            abort(403, f"Sample {id_sample} is not public")
    else:
        user_id, sample = get_user_and_sample_id_by_uuid(uid, id_sample)

        access = SampleController.get_access_mode(user_id, id_sample)
        if access is None:
            abort(403, f"User {user_id} doesn't have the privileges to get data from sample {id_sample}")

        log.info(f'user with {uid = } has requested sample with {id_sample = }')

    message = {'status': 'success',
               'sample': SampleController.filter_description_fields(sample.as_dict())
               }
    result_status = 200
    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")

    # return send_from_directory(sample_page.config['static_folder'], mocked_sample_file)


# ##############################################################
# Sharing samples handling
# ##############################################################

# ##########################
# PUBLIC
# ##########################

@sample_page.route('/<string:step>/<int:step_id>/share/public/', methods=['PUT', 'PATCH'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
#@log_params
@required_token
def make_sample(params: dict, step: str, step_id: int, **kwargs):
    """
    Make public a genomic sequence step. The step is identified by the step name and its id.
    :param params:
    :param step: the genomic step of the sample.
    :param step_id: the sample identifier.
    :return:
    """
    try:
        uid = kwargs['uid']
        user_id = UserController.get_user_by_uid(uid).id

        step = normalize(step)

        log.info(f"User {user_id} makes public {step} {step_id}")
        SampleController.make_public(step, step_id, user_id)
        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


# ##########################
# USERS
# ##########################
@sample_page.route('/<string:step>/<int:step_id>/share/user/', methods=['PUT', 'PATCH'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def share_sample_user(params: dict, step: str, step_id: int, **kwargs):
    """
    Share a sample with another user. An user, owner of the sample, shares the sample with
    another user. A sample_id and an user_id (the invited user) are needed, also the access mode, that can be
    read o readwrite.
    :param step: the genomic step of to take into account.
    :param step_id: the step identifier.
    :param params:
        The data is received in a json format, with the following fields:

            * step_id: the sample identifier, the integer unique identifier of the sample.
            * user_id: the user with which share the sample.
            * readwrite: True if the sample can be modified by user_id.

    :return:
    """
    try:
        step = normalize(step)

        uid = kwargs['uid']
        owner = UserController.get_user_by_uid(uid).id

        if not is_valid_step(step):
            abort(400, f"Invalid step {step}")

        if 'user_uuid' not in params:
            abort(400, 'No user provided')

        user_uuid = params['user_uuid']
        user_id = UserController.get_user_by_uid(user_uuid).id
        if user_id is None:
            abort(400, 'No invited user provided')

        readwrite = params.get('readwrite', False)

        log.info(f"User {owner} share {step} {step_id} with user {user_id} with "
                 f"{'readwrite' if readwrite else 'readonly'} access")
        SampleController.share_step_user(step, owner, step_id, user_id, readwrite)

        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


@sample_page.route('/<string:step>/<int:step_id>/share/user/<string:user_uuid>/', methods=['DELETE'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def unshare_sample_other_user(params: dict, step:str, step_id: int, user_uuid: int, **kwargs):
    """
    A user, the owner of a sample, stops sharing the sample with another user. A
    sample_id and an id_user (the invited user) are needed.
    :param params:
    :param step: the genomic step of the sample.
    :param step_id: the sequence step identifier, the integer unique identifier of the sample.
    :param user_uuid: the user with which unshare the sample.
    :return:
    """
    try:
        step = normalize(step)

        uid = kwargs['uid']
        owner = UserController.get_user_by_uid(uid).id

        # sample_id = params['sample_id']
        if step_id is None:
            abort(400, 'No sample id provided')

        # id_user = params['user_id']
        user_id = UserController.get_user_by_uid(user_uuid).id
        if user_id is None:
            abort(400, 'No invited user provided')

        log.info(f"User {owner} stops sharing sample {step_id} with user {user_uuid}")
        SampleController.unshare_step_user(step, step_id, user_id)

        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


# ##############
# GROUPS
# ##############

@sample_page.route('/<string:step>/<int:step_id>/share/group/', methods=['PUT', 'PATCH'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def share_step_group(params: dict, step: str, step_id: int, **kwargs):
    """
    Share a sample with a group. A user, owner of the sample, shares the sample with
    a group. A sample_id and a group_id are needed.

    The data has to be in json format with the fields:
    * sample_id: the sample identifier.
    * group_id: the user to share the sample.
    * readwrite: True if the sample can be modified by the members of the group.

    :return:
    """
    try:
        step = normalize(step)

        uid = kwargs['uid']
        owner = UserController.get_user_by_uid(uid).id

        group_id = params.get('group_id', None)
        if group_id is None:
            abort(400, 'Group not provided')

        readwrite = params.get('readwrite', 0)

        log.info(f"User {owner} share sample {step_id} with group {group_id} with "
                 f"{'readwrite' if readwrite else 'readonly'} access")
        SampleController.share_step_group(step, owner, step_id, group_id, readwrite)

        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


@sample_page.route('/<string:step>/<int:step_id>/share/group/<int:group_id>/', methods=['DELETE'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def unshare_step_group(params: dict, step: str, step_id: int, group_id: int, **kwargs):
    """
    Stops sharing the sample with a group. A sample_id and a group_id are needed.
    :param params:
    :param step: the genomic step of the sample.
    :param step_id: the sample identifier.
    :param group_id: the user to share the sample.
    :return:
    """
    try:
        step = normalize(step)
        uid = kwargs['uid']
        owner = UserController.get_user_by_uid(uid).id

        log.info(f"User {owner} ends sharing {step} with id {step_id} with group {group_id}")

        SampleController.unshare_step_group(step, owner, step_id, group_id)

        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")

# ##############################################################
#  End of sharing samples handling
# ##############################################################
