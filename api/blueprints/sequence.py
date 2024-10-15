import datetime
import json

from flask import Blueprint
from flask import Response, request
from flask import abort, send_file
from werkzeug.utils import secure_filename

from api import log
from api.auth import required_token, not_required_token
from api.controllers.SampleController import SampleController
from api.controllers.UserController import UserController
from api.decorators import wrap_error, get_params, log_params
from api.field_utils import exclude_param_files, exclude_forbidden_fields, valid_field, is_valid_sequence, \
    is_valid_step, get_step_table, are_valid_sequence_step, filter_coordinates, filter_floats
from api.utils import normalize
from api.utils import serialize_datetime

sequence_page = Blueprint('sequence_page', __name__)

# limiter = Limiter(get_remote_address)


# ##############################################################
# Genomic sequence steps and Sample handling
# ##############################################################

def validate_sequence_step(sequence: str, step: str):
    """
    Validate the metabolic sequence and the corresponding step. I one of them in not valid, abort the request.
    The sequence has to be a valid sequence and the step has to be a valid step for the sequence.
    :param sequence:
    :param step:
    :return:
    """
    if not is_valid_sequence(sequence):
        abort(400, f"Genomic sequence '{sequence}' is not valid")

    if not are_valid_sequence_step(sequence, step):
        abort(400, f"Step '{step}' is not valid in the genomic sequence '{sequence}'")

    return sequence, step

@sequence_page.route('/<string:step>/', methods=['POST'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def upload_sequence_step(params: dict, step: str, **kwargs):
    """
    This method is used to create a new sequence step.
    A metabolic sequence step has a context: the metabolic sequence to which it belongs. This value has to be provided
    as a parameter.
    :param params:
    :param step:
    :param kwargs:
    :return:
    """
    uid: str = kwargs['uid']
    user_id = UserController.get_user_by_uid(uid).id

    step = normalize(step)
    if step == 'SAMPLE':
        sequence = None
        source_id = None
        if "project_id" in params:
            project_id = params['project_id']
            params.pop('project_id')
        else:
            project_id = None
    else:
        project_id = None
        if 'sequence' not in params:
            abort(400, "Sequence not provided")
        sequence = normalize(params['sequence'])

        sequence, step = validate_sequence_step(sequence, step)
        params.pop('sequence')
        if 'source_id' in params:
            source_id = params['source_id']
            params.pop('source_id')
        else:
            abort(400, "Source id not provided")

    log.info('Request received for uploading a sequence')

    # The fields related to the files are treated in a special way.
    # Then, they are not included in the creation of the sample.
    params = exclude_param_files(params)
    params = exclude_forbidden_fields(params, sequence, step)

    invalid = [fld for fld in params if not valid_field(fld)]
    if len(invalid) == 0:
        try:

            # the creation and update dates are the same, the sequence is new.
            now = datetime.datetime.now()
            params['created'] = now
            params['updated'] = now

            # A new sequence is not public.
            params['is_public'] = False

            # Fix the owner of the sequence to the current owner
            params['user_id'] = user_id

            # The coordinates are provided as strings, convert them to float
            params = filter_coordinates(params)
            # The floats are provided with commas, convert them to dots
            params = filter_floats(params)

            # Fix the step to which the current one is related
            # if a project has been provided, put its id in the sample data
            if project_id is not None:
                params['project_id'] = project_id
            # if a source id has been provided, put it in the step data
            if source_id is not None:
                params['source_id'] = source_id

            sequence_created = SampleController.create_sequence_step(params, sequence, step, user_id)

            message = {'status': 'success',
                       'message': f'{step} created',
                       'sequence_step': SampleController.filter_description_fields(sequence_created)
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


def get_user_and_step_by_uuid(sequence_step, uid, step_id):
    """
    Given a user uid and a step id, return the user id and the sample.
    if the sequence step can be accessed by the user.

    :param sequence_step: the step to be used
    :param uid: the uid of the user
    :param step_id: the id of the step
    :return:
    """
    table = get_step_table(sequence_step)

    user = UserController.get_user_by_uid(uid)
    if user is None:
        abort(400, f'User with uid {uid} not found')
    else:
        user_id = user.id

    step = table.query.filter_by(id=step_id).first()

    if step is None:
        abort(400, f'{step} with id {step_id} not found')

    if SampleController.get_step_access_mode(sequence_step, user_id, step_id) is None:
        abort(403, f"User {user_id} doesn't have access to the sequence step {sequence_step} with id {step_id}")

    return user_id, step


@sequence_page.route('/<string:step>/<int:step_id>/', methods=['PUT', 'PATCH'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def update_fields_step(params: dict, step: str, step_id: int, **kwargs):
    if 'sequence' not in params:
        abort(400, "Genomic sequence not provided")

    sequence = normalize(params['sequence'])
    step = normalize(step)
    sequence, step = validate_sequence_step(sequence, step)
    params.pop('sequence')

    # if 'id' not in params:
    #     abort(400, "step id not provided")

    # step_id = params['id']

    log.info(f'Request received for update the genomic sequence {step} with id {step_id}')

    uid: str = kwargs['uid']

    user_id, sample = get_user_and_step_by_uuid(step, uid, step_id)

    access = SampleController.get_step_access_mode(step, user_id, step_id)

    if access is None or access != 'readwrite':
        abort(403, f"User {user_id} doesn't have the privileges to modify the {step} with id {step_id}")

    # The fields related to the files are treated in a special way.
    # Then, they are not included in the creation of the sample.
    params = exclude_param_files(params)
    params = exclude_forbidden_fields(params)

    invalid = [fld for fld in params if not valid_field(fld)]
    if len(invalid) == 0:
        try:
            step_updated = SampleController.update_sequence_step(sequence, step, step_id, params)
            message = {'status': 'success',
                       'message': '{sequence} sequence step updated',
                       'sample': SampleController.filter_description_fields(step_updated)
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


@sequence_page.route('/<string:step>/<int:step_id>/', methods=['GET'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@not_required_token
def get_step(params: dict, step: str, step_id: int, **kwargs):
    uid: str = kwargs['uid']
    # uid = not_required_token(False)

    table = get_step_table(step)

    if uid is None:
        log.info(f'Request received to get {step_id =} as public sample')
        the_step = SampleController.get_step_by_id(table, step_id)

        if the_step is None:
            abort(400, f'Sequence step {step} with id {step_id} not found')

        if not the_step.is_public:
            abort(403, f"Genomic sequence step {step_id} is not public")
    else:
        user_id, the_step = get_user_and_step_by_uuid(table, uid, step_id)

        access = SampleController.get_access_mode(table, user_id, step_id)
        if access is None:
            abort(403, f"User {user_id} doesn't have the privileges to get data from sample {step_id}")

        log.info(f'user with {uid = } has requested sample with {step_id = }')

    message = {'status': 'success',
               'sample': SampleController.filter_description_fields(the_step.as_dict())
               }
    result_status = 200
    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")

    # return send_from_directory(sequence_page.config['static_folder'], mocked_sample_file)


@sequence_page.route('/<string:step>/<int:step_id>/<string:input_type>/', methods=['PUT', 'PATCH'])
@wrap_error
# # @limiter.limit("100/minute")
# @get_params
# @log_params
@required_token
def upload_step_file(step: str, step_id: int, input_type: str, **kwargs):

    uid: str = kwargs['uid']

    params = dict(request.form)

    if 'sequence' not in params:
        abort(400, "Sequence not provided")

    sequence = normalize(params['sequence'])
    step = normalize(step)

    sequence, step = validate_sequence_step(sequence, step)
    params.pop('sequence')

    log.info(f'Request received for uploading a {step} file')
    try:
        if 'file' not in request.files:
            abort(401, "No file provided")
        file = request.files['file']
        filename = secure_filename(file.filename)

        # user_id, sample = get_user_and_sample_id_by_uuid(uid, step_id)
        user_id = UserController.get_user_by_uid(uid).id
        access = SampleController.get_step_access_mode(step, user_id, step_id)
        if access is None or access != 'readwrite':
            abort(403, f"User {user_id} doesn't have the privileges to modify the {step} {step_id} uploading files")

        SampleController.update_file(sequence, step, step_id, input_type, filename, file)
        message = {'status': 'success',
                   'message': f'file for {input_type} ({filename}) added to sample'
                   }
        result_status = 200
    except Exception as e:
        message = {'status': 'error',
                   'message': str(e)
                   }
        result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")



@sequence_page.route('/<string:step>/<int:step_id>/<string:input_type>/', methods=['GET'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@not_required_token
def get_sample_file(params: dict, step: str, step_id:int, input_type: str, **kwargs):
    uid: str = kwargs['uid']
    # uid = not_required_token(False)
    table = get_step_table(step)

    if uid is None:
        log.info(f'Request received to get file {input_type} from {step =} as public data')
        the_step = SampleController.get_step_by_id(table, step_id)
        if the_step is None:
            abort(400, f'Sequence step {step} with id {step_id} not found')

        if not the_step.is_public:
            abort(403, f'Sequence step {step} is not public')
        else:
            access = "read"
            user_id = 'anonymous' # to be used in the log, as no user has been provided
    else:
        log.info(f'Request received  to get file {input_type} from sequence step {step}')
        user_id, the_step = get_user_and_step_by_uuid(step, uid, step_id)
        access = SampleController.get_access_mode(table, user_id, step_id)

    if access is not None:
        filename, filedata = SampleController.get_file_data(the_step, input_type)
        return send_file(filedata, download_name=filename)
    else:
        abort(403, f'User {user_id} has no access to the sequence step {step}')


# ##############################################################
# Sharing sequence steps handling
# ##############################################################

# ##########################
# PUBLIC
# ##########################

@sequence_page.route('/<string:step>/<int:step_id>/share/public/', methods=['PUT', 'PATCH'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
#@log_params
@required_token
def make_step_public(params: dict, step: str, step_id: int, **kwargs):
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
@sequence_page.route('/<string:step>/<int:step_id>/share/user/', methods=['PUT', 'PATCH'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def share_step_user(params: dict, step: str, step_id: int, **kwargs):
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


@sequence_page.route('/<string:step>/<int:step_id>/share/user/<string:user_uuid>/', methods=['DELETE'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def unshare_step_other_user(params: dict, step:str, step_id: int, user_uuid: str, **kwargs):
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

@sequence_page.route('/<string:step>/<int:step_id>/share/group/', methods=['PUT', 'PATCH'])
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


@sequence_page.route('/<string:step>/<int:step_id>/share/group/<int:group_id>/', methods=['DELETE'])
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
#  End of sharing genomic sequence steps and samples handling
# ##############################################################
