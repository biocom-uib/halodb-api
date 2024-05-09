import datetime
import json
import os
import random

from typing import Optional

from flask import Flask, Response, send_from_directory, jsonify, request
from flask_cors import CORS
from flask_log_request_id import RequestID
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from api import log
from api.auth import required_token

from api.decorators import wrap_error, get_params, log_params

from api.db.db import SQLALCHEMY_DATABASE_URI, DatabaseInstance

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
from api.db.models import Temperature, Ph, Salinity, User

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
def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj
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
        resp = [usr.as_dict() for usr in UserController.list_users()]
        message = json.dumps(resp, default=serialize_datetime)
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

    request_form = json.loads(params)
    new_user = User('')
    new_user.email = request_form['email']
    new_user.name = request_form['name']
    new_user.surname = request_form['surname']
    new_user.uid = request_form['uid']
    if 'password' in request_form:
        new_user.password = request_form['password']
    else:
        new_user.password = ""

    try:
        UserController.create_user(new_user)
        message = {'status': 'success',
                   'message': 'User created',
                   'user': new_user.as_dict()
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
        message = usr.as_dict()
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

    result_status = 200
    message = ''
    request_form = json.loads(request.data)
    try:
        UserController.update_user(uid, request_form)
        updated = UserController.get_user_by_uid(uid)
        message = {'status': 'success',
                   'message': 'User updated',
                   'user': updated.as_dict()
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
@required_token
def get_table_list_by_user(params: dict, table: str, **kwargs):
    """
    Given a user id and a related element (group, experiment, project or sample), return the list of elements related
     to the user.
    :param params:
    :param id: the user id.
    :param table: the table to get the related data.
    :return: the list of elements of the table related to the user.
    """
    uid: str = kwargs['uid']
    user_id = UserController.get_user_by_uid(uid).id

    if table == "groups":
        o2_list = GroupController.get_groups_by_user(user_id)
    # elif table == "users":
    #     o2_list = UserController.get_users_by_user(user_id)
    elif table == "experiments":
        o2_list = ExperimentController.get_experiments_by_user(user_id)
    elif table == "projects":
        o2_list = ProjectController.get_projects_by_user(user_id)
    elif table == "samples":
        o2_list = SampleController.get_samples_by_user(user_id)
    else:
        raise Exception(f"Table {table} not found")

    o2_list = [dict(row._mapping) for row in o2_list]
    return Response(response=json.dumps(o2_list, default=serialize_datetime),
                    status=200,
                    mimetype="application/json")


# ##############################################################
# Experiment handling
# ##############################################################
# To handle an experiment, a project must be provided, because the project is the container of the experiment.
# Also an user must be provided, because the user is the owner of the experiment.
@app.route('/experiment/<project_id>', methods=['GET', 'POST'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def create_experiment(params: dict, project_id:any, **kwargs):
    message = ''
    result_status = 200

    uid: str = kwargs['uid']
    user_id = UserController.get_user_by_uid(uid).id

    if request.method == 'GET':
        log.info(f'Request received for list of experiments related to user {user_id =} and {project_id =}')
        resp = [exp.as_dict() for exp in ExperimentController.get_by_project(user_id, project_id)]
        message = json.dumps(resp, default=serialize_datetime)
        result_status = 200
    elif request.method == 'POST':
        log.info(f'Request received for creating a new experiment for {user_id =} and {project_id =}')
        try:
            new_experiment = ExperimentController.create_experiment(params)
            new_experiment.project_id = project_id
            new_experiment.user_id = user_id

            message = {'status': 'success',
                       'message': 'Experiment created',
                       'user': new_experiment.as_dict()
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

    result_status = 200
    message = ''
    try:
        ExperimentController.update_experiment(id, params)
        updated = ExperimentController.get_experiment_by_id(id)
        message = {'status': 'success',
                   'message': 'Experiment updated',
                   'experiment': updated.as_dict()
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
        resp = [prj.as_dict() for prj in ProjectController.list_projects()]
        message = json.dumps(resp, default=serialize_datetime)
        result_status = 200
    elif request.method == 'POST':
        log.info('Request received for creating a new project')
        try:
            new_project = ProjectController.create_project(params)

            message = {'status': 'success',
                       'message': 'Project created',
                       'project': new_project.as_dict()
                       }
            result_status = 200
            log.info(f'Project with id "{new_project.id}" created')
        except Exception as e:
            message = {'status': 'error',
                       'message': str(e)
                       }
            result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
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
        message = prj.as_dict()
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
                   'project': updated.as_dict()
                   }
        result_status = 200
        log.info(f'Project with id = {updated.id} updated')
    except Exception as e:
        log.info(f'Error updating project with {id = }: {str(e)}')
        message = {'status': 'error',
                   'message': str(e)
                   }
        result_status = 400

    return Response(response=json.dumps(message, default=serialize_datetime),
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
        experiments = ExperimentController.get_by_project(id)
        message = [exp.as_dict() for exp in experiments]
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
# @required_token
def upload_sample(params: dict, **kwargs):
    # TODO: handle the json received
    log.info('Request received for uploading a sample')
    return jsonify({"message": "OK"})


@app.route('/query/sample_list/', methods=['GET'])
@wrap_error
@limiter.limit("100/minute")
# @get_params
# @log_params
# @required_token
def get_sample_list():
    log.info('Request received for list of samples')
    random.seed()
    start = 5
    end = 11 + random.randint(0, 10)
    indexes = list(range(start, end))
    random.shuffle(indexes)

    file = os.path.join(app.config['static_folder'], mocked_sample_file)
    with open(file, 'r') as json_file:
        sample = json.load(json_file)

    samples = [sample.copy() for idx in indexes]
    for idx in range(len(indexes)):
        samples[idx]['id'] = indexes[idx]
        samples[idx]['name'] = samples[idx]['name'] + f'Sample_{indexes[idx]}'

    return Response(json.dumps(samples), mimetype="application/json")


@app.route('/query/sample/<id_sample>/', methods=['GET'])
@wrap_error
@limiter.limit("100/minute")
# @get_params
# @log_params
# @required_token
def get_sample(id_sample: str):
    log.info(f'Requested sample with {id_sample = }')
    return send_from_directory(app.config['static_folder'], mocked_sample_file)


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
        value = element.category
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
    o2 = db.session().query(db.get_table(table)).all()

    o2_list = [dict(row._mapping) for row in o2]

    return Response(response=json.dumps(o2_list),
                    status=200,
                    mimetype="application/json")


# ##############################################################
# Group invitation handling
# ##############################################################
@app.route('/group/invitation/<int:user_id>/<int:group>', methods=['PUT', 'PATCH', 'DELETE'])
@wrap_error
def accept(user_id: int, group: int):
    """
    Accept or reject an invitation to join a group
    :param user_id: the user unique identifier
    :param group: the group identifier
    :return:
    """
    try:
        answer = request.method != 'DELETE'

        log.info(f"The invitation request to user {user_id} to join {group} is {'accept' if answer else 'reject'}ed")
        GroupController.accept_invite(user_id, group, answer)
        result = {"message": "OK"}
    except Exception as e:
        result = {"message": f"ERROR: {e}"}

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


@app.route('/group/invite/<int:owner>/<int:invited>/<int:group>', methods=['POST'])
@wrap_error
def invite(owner: int, invited: int, group: int):
    """
    Invite a user to join a group
    :param owner: the owner of the group
    :param invited: the user to invite
    :param group: the group to join
    :return:
    """
    try:
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

    if table == "users":
        json_resp = json.dumps(new_creation.as_dict(), default=serialize_datetime)
    else:
        json_resp = json.dumps(new_creation.as_dict())

    return Response(response=json_resp,
                    status=200,
                    mimetype="application/json")


@app.route('/test/update/<string:table>/', methods=['PUT', 'PATCH'])
@wrap_error
@get_params
def update_table(params: dict, table: str):
    if table == "groups":
        modification = GroupController.update_group(params)
    elif table == "users":
        modification = UserController.update_user(params)
    elif table == "experiments":
        modification = ExperimentController.update_experiment(params)
    elif table == "projects":
        modification = ProjectController.update_project(params)
    elif table == "samples":
        modification = SampleController.update_sample(params)
    else:
        raise Exception(f"Table {table} not found")

    json_resp = json.dumps(modification.as_dict(), default=serialize_datetime)
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

    json_resp = json.dumps(answer.as_dict(), default=serialize_datetime)
    return Response(response=json_resp,
                    status=200,
                    mimetype="application/json")


@app.route('/test/list/<string:table>/', methods=['GET'])
@wrap_error
def get_table_list(table: str):
    if table == "groups":
        o2_list = GroupController.list_groups()
    elif table == "users":
        o2_list = UserController.list_users()
    elif table == "experiments":
        o2_list = ExperimentController.list_experiments()
    elif table == "projects":
        o2_list = ProjectController.list_projects()
    elif table == "samples":
        o2_list = SampleController.list_samples()
    else:
        raise Exception(f"Table {table} not found")

    result = [x.as_dict() for x in o2_list]
    return Response(response=json.dumps(result, default=serialize_datetime),
                    status=200,
                    mimetype="application/json")


# ##############################################################
# End testing the API
# ##############################################################

if __name__ == "__main__":
    app.run(host="0.0.0.0")
