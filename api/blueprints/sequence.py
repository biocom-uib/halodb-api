import datetime

from flask import Blueprint
from flask import abort, send_file
from flask import request
from werkzeug.utils import secure_filename

from api import log
from api.auth import required_token, not_required_token
from api.controllers.SampleController import SampleController
from api.controllers.UserController import UserController
from api.decorators import wrap_error, get_params, log_params
from api.field_utils import exclude_param_files, exclude_forbidden_fields, valid_field, is_valid_sequence, \
    is_valid_step, get_step_table, are_valid_sequence_step, filter_coordinates, filter_floats
from api.utils import normalize

sequence_page = Blueprint('sequence_page', __name__)

# limiter = Limiter(get_remote_address)


# ##############################################################
# Omic sequence steps and Sample handling
# ##############################################################

def validate_sequence_step(sequence: str, step: str):
    """
    Validate the omic sequence and the corresponding step. If one of them is not valid, abort the request.
    The sequence has to be a valid sequence, and the step has to be a valid step for the sequence.
    :param sequence:
    :param step:
    :return:
    """
    if not is_valid_sequence(sequence):
        abort(400, f"Omic sequence '{sequence}' is not valid")

    if not are_valid_sequence_step(sequence, step):
        abort(400, f"Step '{step}' is not valid in the omic sequence '{sequence}'")

    return sequence, step


@sequence_page.route('/public/<string:step>/', methods=['GET'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@not_required_token
def get_public_sequence_step(step: str):
    """
    This method is used to get the public omic sequence step. The step is identified by its name.
    :param step:
    :return:
    """
    step = normalize(step)
    if not is_valid_step(step):
        abort(400, f"Invalid step {step}")

    log.info(f'Request received for getting public {step} sequence step')

    # The uid is not needed, as the data is public
    public_list = SampleController.get_public_sequence_step(step)

    if public_list is None:
        result = None
    else:
        result = [x['id'] for x in public_list]
    message = {'status': 'success',
               'omic sequence step': step,
               'public_ids': result
               }
    result_status = 200

    return message, result_status

@sequence_page.route('/<string:step>/', methods=['POST'])
@wrap_error
# @limiter.limit("100/minute")
@get_params
@log_params
@required_token
def upload_sequence_step(params: dict, step: str, **kwargs):
    """
    This method is used to create a new omic sequence step. An omic sequence step has a context: the omic sequence to which it belongs. This value has to be provided
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

    # The fields related to the files are treated specially.
    # Then, they are not included in the creation of the omic sequence step.
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
                       'step': SampleController.filter_description_fields(sequence_created)
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

    #return json.dumps(message, default=str), result_status
    return message, result_status


def get_user_and_step_by_uuid(sequence_step, uid, step_id):
    """
    Given a user uid and a step id, return the user id and the step data,
    if the user can access the sequence step.

    :param sequence_step: The step to be used
    :param uid: The uid of the user
    :param step_id: The id of the step
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

    step = normalize(step)
    if step != 'SAMPLE' and 'sequence' not in params:
        abort(400, "Omic sequence not provided")

    if 'sequence' in params:
        sequence = normalize(params['sequence'])
        sequence, step = validate_sequence_step(sequence, step)
        params.pop('sequence')
    else:
        sequence = None

    # if 'id' not in params:
    #     abort(400, "step id not provided")

    # step_id = params['id']

    log.info(f'Request received for update the omic sequence {step} with id {step_id}')

    uid: str = kwargs['uid']

    user_id, _ = get_user_and_step_by_uuid(step, uid, step_id)

    access = SampleController.get_step_access_mode(step, user_id, step_id)

    if access is None or access != 'readwrite':
        abort(403, f"User {user_id} doesn't have the privileges to modify the {step} with id {step_id}")

    # The fields related to the files are treated specially.
    # Then, they are not included in the creation of the omic sequence step.
    params = exclude_param_files(params)
    params = exclude_forbidden_fields(params)

    invalid = [fld for fld in params if not valid_field(fld)]
    if len(invalid) == 0:
        try:
            step_updated = SampleController.update_sequence_step(sequence, step, step_id, params)
            message = {'status': 'success',
                       'message': f'{sequence} sequence {step} with id {step_id} updated',
                       step: SampleController.filter_description_fields(step_updated)
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

    #return json.dumps(message, default=str), result_status
    return message, result_status


@sequence_page.route('/<string:step>/<int:step_id>/', methods=['GET'])
@wrap_error
# @limiter.limit("100/minute")
# get_params
# @log_params
@not_required_token
def get_step(step: str, step_id: int, **kwargs):
    uid: str = kwargs['uid']
    # uid = not_required_token(False)

    step = normalize(step)
    table = get_step_table(step)

    if uid is None:
        log.info(f'Request received to get {step_id =} as public {step}')
        the_step = SampleController.get_step_by_id(table, step_id)

        if the_step is None:
            abort(400, f'Sequence step {step} with id {step_id} not found')

        if not the_step.is_public:
            abort(403, f"Omic sequence step {step} with id {step_id} is not public")
    else:
        user_id, the_step = get_user_and_step_by_uuid(step, uid, step_id)

        access = SampleController.get_access_mode(table, user_id, step_id)
        if access is None:
            abort(403, f"User {user_id} doesn't have the privileges to get data from {step} {step_id}")

        log.info(f'user with {uid = } has requested {step} with {step_id = }')

    message = {'status': 'success',
               step: SampleController.filter_description_fields(the_step.as_dict())
               }
    result_status = 200

    return message, result_status


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

        user_id = UserController.get_user_by_uid(uid).id
        access = SampleController.get_step_access_mode(step, user_id, step_id)
        if access is None or access != 'readwrite':
            abort(403, f"User {user_id} doesn't have the privileges to modify the {step} {step_id} uploading files")

        SampleController.update_file(sequence, step, step_id, input_type, filename, file)
        message = {'status': 'success',
                   'message': f'file for {input_type} ({filename}) added to  the {step} {step_id}'
                   }
        result_status = 200
    except Exception as e:
        message = {'status': 'error',
                   'message': str(e)
                   }
        result_status = 400

    #return json.dumps(message, default=serialize_datetime), result_status
    return message, result_status


@sequence_page.route('/<string:step>/<int:step_id>/<string:input_type>/', methods=['GET'])
@wrap_error
# @limiter.limit("100/minute")
# @get_params
# @log_params
@not_required_token
def get_step_file(step: str, step_id:int, input_type: str, **kwargs):
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
        return send_file(filedata, download_name=filename), 200


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
# @get_params
#@log_params
@required_token
def make_step_public(step: str, step_id: int, **kwargs):
    """
    Make public an omic sequence step. The step is identified by the step name and its id.

    :param step: The omic sequence step to be shared.
    :param step_id: The step identifier.
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

    #return json.dumps(result) ,200
    return result ,200

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
    Share an omic sequence step with another user. A user, owner of a concrete step, shares it with
    another user. A step_id and a user_id (the invited user) are needed, also the access mode, that can be
    read o readwrite.
    :param step: The omic step of to take into account.
    :param step_id: The step identifier.
    :param params:
        The data is received in a JSON format, with the following fields:

            * step_id: the integer unique identifier of the step.
            * user_id: the user with which to share the step.
            * readwrite: True if the invited user can modify the step.

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

    #return json.dumps(result), 200
    return result, 200


@sequence_page.route('/<string:step>/<int:step_id>/share/user/<string:user_uuid>/', methods=['DELETE'])
@wrap_error
# @limiter.limit("100/minute")
# @get_params
# @log_params
@required_token
def unshare_step_other_user(step:str, step_id: int, user_uuid: str, **kwargs):
    """
    A user, the owner of a metabolic sequence step, stops sharing the step with another user. A
    step and an id_user (the invited user) are needed.

    :param step: The omic step of the omic sequence step.
    :param step_id: The sequence step identifier, the integer unique identifier of the step.
    :param user_uuid: The user with which to unshare the step.
    :return:
    """
    try:
        step = normalize(step)

        uid = kwargs['uid']
        owner = UserController.get_user_by_uid(uid).id

        # step_id = params['step_id']
        if step_id is None:
            abort(400, 'No omic sequence step id provided')

        # id_user = params['user_id']
        user_id = UserController.get_user_by_uid(user_uuid).id
        if user_id is None:
            abort(400, 'No invited user provided')

        log.info(f"User {owner} stops sharing omic sequence step {step_id} with user {user_uuid}")
        SampleController.unshare_step_user(step, step_id, user_id)

        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    #return json.dumps(result), 200
    return result, 200


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
    Share an omic sequence step with a group. A user, owner of the omic sequence step, shares the step with
    a group. A step_id and a group_id are needed.

    The data has to be in JSON format with the fields:
    * step_id: the omic sequence step identifier.
    * group_id: the with which to share the step.
    * readwrite: True if the step can be modified by the members of the group, or they are only allowed to read the
                 corresponding data.

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

        log.info(f"User {owner} shares omic sequence step {step_id} with group {group_id} with "
                 f"{'readwrite' if readwrite else 'readonly'} access")
        SampleController.share_step_group(step, owner, step_id, group_id, readwrite)

        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    #return json.dumps(result), 200
    return result, 200


@sequence_page.route('/<string:step>/<int:step_id>/share/group/<int:group_id>/', methods=['DELETE'])
@wrap_error
# @limiter.limit("100/minute")
# @get_params
# @log_params
@required_token
def unshare_step_group(step: str, step_id: int, group_id: int, **kwargs):
    """
    Stops sharing the metabolic sequence step with a group. A step_id and a group_id are needed.
    :param step: The omic sequence step to be considered.
    :param step_id: The step identifier.
    :param group_id: The user with which to share the data.
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

    #return json.dumps(result), 200
    return result, 200

# ##############################################################
#  End of sharing omic sequence steps and samples handling
# ##############################################################
