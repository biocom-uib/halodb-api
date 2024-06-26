import datetime
import decimal
import json
import os
import random
from typing import Optional

from flask import Flask, Response, send_from_directory, jsonify, request, make_response, abort, send_file
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_log_request_id import RequestID
from werkzeug.utils import secure_filename

from api import log
from api.auth import required_token, verify_token
from api.db.db import SQLALCHEMY_DATABASE_URI, DatabaseInstance
from api.decorators import wrap_error, get_params, log_params
from api.utils import to_dict

# from api.db.models  # Do not import yet, the database must be initialized first


app = Flask(__name__)
CORS(app)
RequestID(app)
limiter = Limiter(get_remote_address, app=app)

log.setup_logger(app, gunicorn=__name__ != '__main__')

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['static_folder'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'static')

mocked_sample_file = 'sample42.json'

log.info('Waiting for the database to be ready')
db = DatabaseInstance.wait_for_connection_and_create_instance(wait_time=5, attempts=-1)

if db is not None:
    log.info('The database is ready')
    db.init_app(app)
else:
    log.error('The database could not be initialized')

# This has to be imported here
from api.db.models import Temperature, Ph, Salinity, Sample

from api.controllers.UserController import UserController
from api.controllers.GroupController import GroupController
from api.controllers.ExperimentController import ExperimentController
from api.controllers.ProjectController import ProjectController
from api.controllers.SampleController import SampleController


@app.route("/")
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def dummy(params: dict, email: Optional[str] = None, **kwargs):
    log.info(f"Request received for { email = } with { params = }")
    return {"message": "OK"}


# Define a custom function to serialize datetime objects

def serialize_datetime(value):
    if isinstance(value, (datetime.date, datetime.time, datetime.datetime)):
        return value.isoformat()
    elif isinstance(value, datetime.timedelta):
        return str(value)
    elif isinstance(value, decimal.Decimal):
        return str(value)
    return value

    # raise TypeError("Type not serializable")


@app.route('/users/', methods=['GET'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
def users(params: dict, **kwargs):
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


@app.route('/user/', methods=['POST'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
# @required_token
def add_user(params: dict, **kwargs):
    log.info('Request received for creating a new user')

    try:
        new_user = UserController.create_user(params)
        message = {'status': 'success',
                   'message': 'User created',
                   'user': new_user
                   }
        result_status = 200
        log.info(f'User with uid "{new_user.uid}" created')
    except Exception as e:
        message = {'status': 'error',
                   'message': str(e)
                   }
        result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")


@app.route('/user/', methods=['GET', 'DELETE'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
# @required_token
def user_handle(params: dict, **kwargs):
    result_status = 200
    message = ''

    uid: str = kwargs['uid']

    if request.method == 'GET':
        log.info(f'GET request received for user { uid = } with { params = }')
        usr = UserController.get_user_by_uid(uid)
        message = usr
        result_status = 200

    if request.method == 'DELETE':
        log.info(f'DELETE request received for user { uid = }')
        try:
            UserController.delete_user(uid)
            message = {'status': 'success',
                       'message': 'User deleted'
                       }
            result_status = 200
            log.info(f'User with {uid = } deleted')
        except Exception as e:
            log.info(f'Error deleting user with {uid = }: {str(e)}')
            message = {'status': 'error',
                       'message': str(e)
                       }
            result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")


@app.route('/user/', methods=['PUT', 'PATCH'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
# @required_token
def user_edit(params: dict, **kwargs):
    uid: str = kwargs['uid']

    log.info(f'PUT/PATCH request received for user {uid = } with {params = }')

    request_form = json.loads(request.data)
    try:
        UserController.update_user(uid, request_form)
        updated = UserController.get_user_by_uid(uid)
        message = {'status': 'success',
                   'message': 'User updated',
                   'user': updated
                   }
        result_status = 200
        log.info(f'User with id = {updated.id} updated')
    except Exception as e:
        log.info(f'Error updating user with {uid = }: {str(e)}')
        message = {'status': 'error',
                   'message': str(e)
                   }
        result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")


# ##############################################################
#  Querying information related to a user
# ##############################################################
@app.route('/user/list/<string:table>/', methods=['GET'])
@get_params
@wrap_error
# @required_token
def get_table_list_by_user(params: dict, table: str, **kwargs):
    """
    Given a user id and a related element (group, experiment, project or sample), return the list of elements related
     to the user. If no valid token, and the query is for samples, the list of public samples is returned.
    :param params:
    :param id: the user id.
    :param table: the table to get the related data.
    :return: the list of elements of the table related to the user. Or the list of public samples
    """
    uid = get_uid_from_request(False)
    if uid is None:
        if table == 'samples':
            log.info('Request received for list of public samples')
            result = SampleController.list_public_samples()
        else:
            abort(403, "No token provided")
    else:
        # uid: str = kwargs['uid']
        user_id = UserController.get_user_by_uid(uid).id

        if table == "groups":
            result = GroupController.get_groups_by_user(user_id)
        # elif table == "users":
        #     result = UserController.get_users_by_user(user_id)
        elif table == "experiments":
            result = ExperimentController.get_experiments_by_user(user_id)
        elif table == "projects":
            result = ProjectController.get_projects_by_user(user_id)
        elif table == "samples":
            result = SampleController.get_samples_shared_with_user(user_id)
        else:
            abort(405, f"Table {table} not found")

    return Response(response=json.dumps(result, default=serialize_datetime),
                    status=200,
                    mimetype="application/json")


# ##############################################################
# Experiment handling
# ##############################################################
# To handle an experiment, a project must be provided, because the project is the container of the experiment.
# Also, a user must be provided, because the user is the owner of the experiment.
@app.route('/experiment/<project_id>', methods=['GET', 'POST'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def create_experiment(params: dict, project_id: any, **kwargs):
    message = ''
    result_status = 200

    uid: str = kwargs['uid']
    user_id = UserController.get_user_by_uid(uid).id

    if request.method == 'GET':
        log.info(f'Request received for list of experiments related to user {user_id =} and {project_id =}')
        resp = ExperimentController.get_by_project(user_id, project_id)
        message = json.dumps(resp, default=serialize_datetime)
        result_status = 200
    elif request.method == 'POST':
        log.info(f'Request received for creating a new experiment for {user_id =} and {project_id =}')
        try:
            new_experiment = ExperimentController.create_experiment(user_id, params)
            new_experiment.project_id = project_id
            new_experiment.user_id = user_id

            message = {'status': 'success',
                       'message': 'Experiment created',
                       'user': new_experiment
                       }
            result_status = 200
            log.info(f'Experiment with id "{new_experiment.id}" created')
        except Exception as e:
            message = {'status': 'error',
                       'message': str(e)
                       }
            result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")


@app.route('/experiment/<int:id>/', methods=['GET', 'DELETE'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def experiment_handle(params: dict, id: Optional[int] = None, **kwargs):
    result_status = 200
    message = ''

    uid: str = kwargs['uid']
    user_id = UserController.get_user_by_uid(uid).id

    exp = ExperimentController.get_experiment_by_id_user_id(id, user_id)

    if exp is None:
        message = {'status': 'error',
                   'message': f"User {user_id} is not the owner of the experiment {id}"
                   }
        result_status = 400
    else:
        if request.method == 'GET':
            log.info(f'GET request received for experiment {id = } with {params = }')
            exp = ExperimentController.get_experiment_by_id(id)

        if request.method == 'DELETE':
            log.info(f'DELETE request received for experiment {id = }')
            try:
                ExperimentController.delete_experiment(id)
                message = {'status': 'success',
                           'message': 'Experiment deleted'
                           }
                result_status = 200
                log.info(f'Experiment with {id = } deleted')
            except Exception as e:
                log.info(f'Error deleting experiment with {id = }: {str(e)}')
                message = {'status': 'error',
                           'message': str(e)
                           }
                result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")


@app.route('/experiment/<int:id>', methods=['PUT', 'PATCH'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def experiment_edit(params: dict, id: Optional[int] = None, **kwargs):
    log.info(f'PUT/PATCH request received for experiment {id = } with {params = }')

    try:
        ExperimentController.update_experiment(id, params)
        updated = ExperimentController.get_experiment_by_id(id)
        message = {'status': 'success',
                   'message': 'Experiment updated',
                   'experiment': updated
                   }
        result_status = 200
        log.info(f'Experiment with id = {updated.id} updated')
    except Exception as e:
        log.info(f'Error updating experiment with {id = }: {str(e)}')
        message = {'status': 'error',
                   'message': str(e)
                   }
        result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")


# ##############################################################
# Project handling
# ##############################################################
@app.route('/project/', methods=['GET', 'POST'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def create_project(params: dict, **kwargs):
    # TODO: link to user
    message = ''
    result_status = 200

    if request.method == 'GET':
        log.info('Request received for list of projects')
        resp = ProjectController.list_projects()
        message = json.dumps(resp, default=serialize_datetime)
        result_status = 200
    elif request.method == 'POST':
        log.info('Request received for creating a new project')
        try:
            new_project = ProjectController.create_project(params)

            message = {'status': 'success',
                       'message': 'Project created',
                       'project': new_project
                       }
            result_status = 200
            log.info(f'Project with id "{new_project.id}" created')
        except Exception as e:
            message = {'status': 'error',
                       'message': str(e)
                       }
            result_status = 400

    # return Response(response=json.dumps(message, default=serialize_datetime),
    return Response(response=json.dumps(message, default=str),
                    status=result_status,
                    mimetype="application/json")


@app.route('/project/<int:id>/', methods=['GET', 'DELETE'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def project_handle(params: dict, id: Optional[int] = None, **kwargs):
    # TODO: link to user
    result_status = 200
    message = ''

    if request.method == 'GET':
        log.info(f'GET request received for project {id = } with {params = }')
        prj = ProjectController.get_project_by_id(id)
        message = prj
        result_status = 200

    if request.method == 'DELETE':
        log.info(f'DELETE request received for project {id = }')
        try:
            ProjectController.delete_project(id)
            message = {'status': 'success',
                       'message': 'Project deleted'
                       }
            result_status = 200
            log.info(f'Project with {id = } deleted')
        except Exception as e:
            log.info(f'Error deleting project with {id = }: {str(e)}')
            message = {'status': 'error',
                       'message': str(e)
                       }
            result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")


@app.route('/project/<int:id>', methods=['PUT', 'PATCH'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def project_edit(params: dict, id: Optional[int] = None, **kwargs):
    # TODO: link to user
    log.info(f'PUT/PATCH request received for project {id = } with {params = }')

    result_status = 200
    message = ''
    try:
        ProjectController.update_project(id, params)
        updated = ProjectController.get_project_by_id(id)
        message = {'status': 'success',
                   'message': 'Project updated',
                   'project': updated
                   }
        result_status = 200
        log.info(f'Project with id = {updated.id} updated')
    except Exception as e:
        log.info(f'Error updating project with {id = }: {str(e)}')
        message = {'status': 'error',
                   'message': str(e)
                   }
        result_status = 400

    # return Response(response=json.dumps(message, default=serialize_datetime),
    return Response(response=json.dumps(message, default=str),
                    status=result_status,
                    mimetype="application/json")


@app.route('/project/<int:id>/list/', methods=['GET'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def project_get_experiments(params: dict, id: Optional[int] = None, **kwargs):
    # TODO: link to user
    result_status = 200
    message = ''

    if request.method == 'GET':
        log.info(f'GET request received for experiments in project {id = } with {params = }')
        experiments = ExperimentController.get_by_project(id, params['project_id'])
        message = experiments
        result_status = 200

    return Response(response=json.dumps(message, default=serialize_datetime),
                    status=result_status,
                    mimetype="application/json")


# ##############################################################
# Sample handling
# ##############################################################
@app.route('/upload/sample/', methods=['POST'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def upload_sample(params: dict, **kwargs):
    log.info('Request received for uploading a sample')
    uid: str = kwargs['uid']
    user_id = UserController.get_user_by_uid(uid).id
    # The fields related to the files are treated in a special way.
    # Then, they are not included in the creation of the sample.
    params = Sample.exclude_param_files(params)
    params = Sample.exclude_forbidden_fields(params)

    invalid = [fld for fld in params if not Sample.valid_field(fld)]
    if len(invalid) == 0:
        try:
            # the creation and update dates are the same, the sample is new.
            now = datetime.datetime.now()
            params['created'] = now
            params['updated'] = now

            # A new sample is not public.
            params['is_public'] = False

            # Fix the owner of the sample to the current owner
            params['user_id'] = user_id

            sample_created = SampleController.create_sample(params)

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

    # access_mode = SampleController.get_access_mode(user_id, id_sample)
    # if access_mode is None:
    #    abort(403, f"User {user_id} doesn't have access to sample {id_sample}")

    return user_id, sample


@app.route('/query/sample/<int:id_sample>/<input_type>/', methods=['GET'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
# @required_token
def get_sample_file(params: dict, id_sample: int, input_type: str, **kwargs):
    # uid: str = kwargs['uid']
    uid = get_uid_from_request(False)

    if uid is None:
        log.info(f'Request received to get file {input_type} from {id_sample =} as public sample')
        sample = SampleController.get_sample_by_id(id_sample)
        if not sample.is_public:
            abort(403, f"Sample {id_sample} is not public")
        else:
            access = "read"
    else:
        log.info(f'Request received  to get file {input_type} from sample {id_sample}')
        user_id, sample = get_user_and_sample_id_by_uuid(uid, id_sample)
        access = SampleController.get_access_mode(user_id, id_sample)

    if access is not None:
        filename, filedata = sample.get_file_data(input_type)
        return send_file(filedata, download_name=filename)
    else:
        abort(403, f'User {user_id} has no access the sample {id_sample}')


@app.route('/upload/sample/<int:id_sample>', methods=['PUT', 'PATCH'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def update_fields_sample(params: dict, id_sample: int, **kwargs):
    log.info('Request received for update a sample')
    uid: str = kwargs['uid']

    user_id, sample = get_user_and_sample_id_by_uuid(uid, id_sample)

    user_id, sample = get_user_and_sample_id_by_uuid(uid, id_sample)
    access = SampleController.get_access_mode(user_id, id_sample)
    if access is None or access != 'readwrite':
        abort(403, f"User {user_id} doesn't have the privileges to modify the sample {id_sample}")

    # The fields related to the files are treated in a special way.
    # Then, they are not included in the creation of the sample.
    params = Sample.exclude_param_files(params)
    params = Sample.exclude_forbidden_fields(params)

    invalid = [fld for fld in params if not Sample.valid_field(fld)]
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


def get_uid_from_request(required: bool = False):
    """
    Get the user id from the request. If the token is not present, return None if required is False, otherwise abort.
    :param required: True if it's mandatory to have a valid token to proceed. In this case if no token is provided, abort.
    :return: the uid or None if no token is provided and required is False.
    """
    token = request.headers.get('Authorization')
    if not token:
        if required:
            abort(403, 'No token provided')
        return None
    if not token.startswith('Bearer '):
        abort(403, 'Invalid token type')

    decoded_token = verify_token(token.split(' ')[1])
    return decoded_token['uid']


@app.route('/upload/sample/<int:id_sample>/<input_type>', methods=['PUT', 'PATCH'])
@wrap_error
# @limiter.limit("100/minute")
# @get_params
# @log_params
# @required_token
def upload_sample_file(id_sample: int, input_type: str):
    log.info('Request received for uploading a sample file')
    try:
        if 'file' not in request.files:
            abort(401, "No file provided")
        file = request.files['file']
        filename = secure_filename(file.filename)

        uid = get_uid_from_request(True)

        user_id, sample = get_user_and_sample_id_by_uuid(uid, id_sample)
        access = SampleController.get_access_mode(user_id, id_sample)
        if access is None or access != 'readwrite':
            abort(403, f"User {user_id} doesn't have the privileges to modify the sample {id_sample}")

        SampleController.update_file(id_sample, input_type, filename, file)
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


@app.route('/query/sample/<int:id_sample>/', methods=['GET'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
# @required_token
def get_sample(params: dict, id_sample: int, **kwargs):
    # uid: str = kwargs['uid']
    uid = get_uid_from_request(False)

    if uid is None:
        log.info(f'Request received to get {id_sample =} as public sample')
        sample = SampleController.get_sample_by_id(id_sample)
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

    # return send_from_directory(app.config['static_folder'], mocked_sample_file)


# ##############################################################
# Category handling
# ##############################################################
@app.route('/query/<string:table>/<float:value>', methods=['GET'])
@wrap_error
@limiter.limit("100/minute")
# @get_params
# @log_params
# @required_token
def get_classification_data(table: str, value: float):
    """
    Given a table and a value, return the corresponding category.
    :param table: the categories table where look for the value
    :param value: the value to be categorized
    :return:
    """
    if table == 'temperature':
        element = Temperature.query.filter(Temperature.vmin < value, value <= Temperature.vmax).first()
    elif table == 'ph':
        element = Ph.query.filter(Ph.vmin < value, value <= Ph.vmax).first()
    elif table == 'salinity':
        element = Salinity.query.filter(Salinity.vmin < value, value <= Salinity.vmax).first()
    else:
        element = None
    if element is not None:
        value = element.description
    else:
        value = None
    return jsonify(value)


@app.route('/query/<string:table>/')
@wrap_error
@limiter.limit("100/minute")
# @get_params
# @log_params
# @required_token
def get_table_data(table: str):
    """
    Given a classification, return the set of its categories and the corresponding range
    :param table: the classification to be returned
    :return:
    """
    # o2 = db.session().query(db.get_table(table)).all()
    with DatabaseInstance.get().session() as session:
        o2 = session.query(db.get_table(table)).all()

    o2_list = [dict(row._mapping) for row in o2]

    return Response(response=json.dumps(o2_list),
                    status=200,
                    mimetype="application/json")


# ##############################################################
# Sharing samples handling
# ##############################################################

# ##########################
# PUBLIC
# ##########################

@app.route('/share/public/<int:sample_id>', methods=['PUT', 'PATCH'])
@wrap_error
@limiter.limit("100/minute")
#@get_params
#@log_params
@required_token
def make_sample_public(sample_id: int, **kwargs):
    """
    Make public a sample
    :param params:
    :param sample_id: the sample identifier.
    :return:
    """
    try:
        uid = kwargs['uid']
        user_id = UserController.get_user_by_uid(uid).id

        log.info(f"User {user_id} makes public sample {sample_id}")
        SampleController.make_public(sample_id, user_id)
        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


# ##########################
# USERS
# ##########################
@app.route('/share/user/', methods=['POST'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def share_sample_user(params: dict, **kwargs):
    """
    Share a sample with another user. An user, owner of the sample, shares the sample with
    another user. A sample_id and an user_id (the invited user) are needed, also the access mode, that can be
    read o readwrite.
    The data is received in a json format, with the following fields:

        * id_sample: the sample identifier, the integer unique identifier of the sample.
        * user_id: the user with which share the sample.
        * readwrite: True if the sample can be modified by user_id.

    :param params:
    :return:
    """
    try:
        uid = kwargs['uid']
        owner = UserController.get_user_by_uid(uid).id

        sample_id = params.get('sample_id', None)
        if sample_id is None:
            abort(400, 'No sample id provided')

        user_id = params.get('user_id', None)
        if user_id is None:
            abort(400, 'No invited user provided')

        readwrite = params.get('readwrite', False)

        log.info(f"User {owner} share sample {sample_id} with user {user_id} with "
                 f"{'readwrite' if readwrite else 'readonly'} access")
        SampleController.share_sample_user(owner, sample_id, user_id, readwrite)

        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


@app.route('/share/user/<int:sample_id>/<int:id_user>', methods=['DELETE'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def unshare_sample_other_user(params: dict, sample_id: int, id_user: int, **kwargs):
    """
    A user, the owner of a sample, stops sharing the sample with another user. A
    sample_id and an id_user (the invited user) are needed.
    :param params:
    :param sample_id: the sample identifier, the integer unique identifier of the sample.
    :param id_user: the user with which share the sample.
    :return:
    """
    try:
        uid = kwargs['uid']
        owner = UserController.get_user_by_uid(uid).id

        # sample_id = params['sample_id']
        if sample_id is None:
            abort(400, 'No sample id provided')

        # id_user = params['user_id']
        if id_user is None:
            abort(400, 'No invited user provided')

        log.info(f"User {owner} stops sharing sample {sample_id} with user {id_user}")
        SampleController.unshare_sample_user(sample_id, id_user)

        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


@app.route('/share/user/<int:sample_id>', methods=['DELETE'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def unshare_sample_user(params: dict, sample_id: int, **kwargs):
    """
    Unshare a sample which has been shared with the current user by another user.
    :param params:
    :param sample_id: the sample identifier.
    :return:
    """
    try:
        uid = kwargs['uid']
        user_id = UserController.get_user_by_uid(uid).id

        log.info(f"User {user_id} doesn't have interest on sample {sample_id}")
        SampleController.unshare_sample_user(sample_id, user_id)
        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


# ##############
# GROUPS
# ##############

@app.route('/share/group/', methods=['POST'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def share_sample_group(params: dict, **kwargs):
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
        uid = kwargs['uid']
        owner = UserController.get_user_by_uid(uid).id

        sample_id = params.get('sample_id', None)
        if sample_id is None:
            abort(400, 'No sample id provided')

        group_id = params.get('group_id', None)
        if group_id is None:
            abort(400, 'Group not provided')

        readwrite = params.get('readwrite', 0)

        log.info(f"User {owner} share sample {sample_id} with group {group_id} with "
                 f"{'readwrite' if readwrite else 'readonly'} access")
        SampleController.share_sample_group(owner, sample_id, group_id, readwrite)

        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


@app.route('/share/group/<int:sample_id>/<int:group_id>', methods=['DELETE'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def unshare_sample_group(params: dict, sample_id: int, group_id: int, **kwargs):
    """
    Stops sharing the sample with a group. A sample_id and a group_id are needed.
    :param params:
    :param sample_id: the sample identifier.
    :param group_id: the user to share the sample.
    :return:
    """
    try:
        uid = kwargs['uid']
        owner = UserController.get_user_by_uid(uid).id

        log.info(f"User {owner} stops sharing sample {sample_id} with group {group_id}")

        SampleController.unshare_sample_group(owner, sample_id, group_id)

        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


# ##############################################################
#  End of sharing samples handling
# ##############################################################

# ##############################################################
# Group invitation handling
# ##############################################################
@app.route('/group/invitation/<int:group>', methods=['PUT', 'PATCH', 'DELETE'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def accept(params: dict, group: int, **kwargs):
    """
    Accept or reject an invitation to join a group
    :param params:
    :param group: the group identifier
    :return:
    """
    try:
        uid = kwargs['uid']
        user_id = UserController.get_user_by_uid(uid).id

        answer = request.method != 'DELETE'

        log.info(f"The invitation request to user {user_id} to join {group} is {'accept' if answer else 'reject'}ed")
        GroupController.accept_invite(user_id, group, answer)
        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


@app.route('/group/invite/<int:invited>/<int:group>', methods=['POST'])
@wrap_error
def invite(params: dict, invited: int, group: int, **kwargs):
    """
    Invite a user to join a group
    :param params:
    :param invited: the user to invite
    :param group: the group to join
    :return:
    """
    try:
        uid = kwargs['uid']
        owner = UserController.get_user_by_uid(uid).id

        log.info(f"Invitation request from user {owner} to user {invited} to join group {group}")
        GroupController.invite(owner, invited, group)
        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


# ##############################################################
# Testing the API
#    The following endpoints are used to test the API.
#    They will be removed.
# ##############################################################
@app.route('/test/create/<string:table>/', methods=['POST'])
@wrap_error
@get_params
def create_table(params: dict, table: str):
    if table == "groups":
        new_creation = GroupController.create_group(params)
    elif table == "users":
        new_creation = UserController.create_user(params)
    elif table == "experiments":
        new_creation = ExperimentController.create_experiment(params)
    elif table == "projects":
        new_creation = ProjectController.create_project(params)
    elif table == "samples":
        new_creation = SampleController.create_sample(params)
    else:
        raise Exception(f"Table {table} not found")

    json_resp = json.dumps(new_creation, default=str)
    return Response(response=json_resp,
                    status=200,
                    mimetype="application/json")


@app.route('/test/update/<string:table>/', methods=['PUT', 'PATCH'])
@wrap_error
@get_params
def update_table(params: dict, table: str):
    if table == "groups":
        modification = GroupController.update_group(1, params)
    elif table == "users":
        modification = UserController.update_user(20, params)
    elif table == "experiments":
        modification = ExperimentController.update_experiment(20, params)
    elif table == "projects":
        modification = ProjectController.update_project(1, params)
    elif table == "samples":
        modification = SampleController.update_sample(1, params)
    else:
        raise Exception(f"Table {table} not found")

    json_resp = json.dumps(modification, default=serialize_datetime)
    return Response(response=json_resp,
                    status=200,
                    mimetype="application/json")


@app.route('/test/query/<string:table>/<int:id>', methods=['GET'])
@wrap_error
@get_params
def query_table(params: dict, table: str, id: int):
    if table == "groups":
        answer = GroupController.get_group_by_id(id)
    elif table == "users":
        answer = UserController.get_user(id)
    elif table == "experiments":
        answer = ExperimentController.get_experiment_by_id(id)
    elif table == "projects":
        answer = ProjectController.get_project_by_id(id)
    elif table == "samples":
        answer = SampleController.get_sample_by_id(id)
    else:
        raise Exception(f"Table {table} not found")

    json_resp = json.dumps(answer, default=serialize_datetime)
    return Response(response=json_resp,
                    status=200,
                    mimetype="application/json")


@app.route('/test/list/<string:table>/', methods=['GET'])
@wrap_error
def get_table_list(table: str):
    if table == "groups":
        result = GroupController.list_groups()
    elif table == "users":
        result = UserController.list_users()
    elif table == "experiments":
        result = ExperimentController.list_experiments(1)
    elif table == "projects":
        result = ProjectController.list_projects()
    elif table == "samples":
        result = SampleController.list_samples()
    else:
        raise Exception(f"Table {table} not found")

    return Response(response=json.dumps(result, default=serialize_datetime),
                    status=200,
                    mimetype="application/json")


# ##############################################################
# End testing the API
# ##############################################################

if __name__ == "__main__":
    app.run(host="0.0.0.0")
