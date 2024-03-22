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
from sqlalchemy import DateTime, func

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
    raise TypeError("Type not serializable")


@app.route('/users/', methods=['GET', 'POST'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
# @required_token
def users():
    message = ''
    result_status = 200

    if request.method == 'GET':
        log.info('Request received for list of users')
        resp = [usr.as_dict() for usr in UserController.list_users()]
        message = json.dumps(resp, default=serialize_datetime)
        result_status = 200
    elif request.method == 'POST':
        log.info('Request received for creating a new user')
        # request_form = request.form.to_dict()
        request_form = json.loads(request.data)
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


@app.route('/user/<string:uid>/', methods=['GET', 'DELETE'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
# @required_token
def user_handle(params: dict, uid: Optional[str] = None, **kwargs):

    result_status = 200
    message = ''

    if request.method == 'GET':
        log.info(f'GET request received for { uid = } with { params = }')
        usr = UserController.get_user_by_uid(uid)
        message = usr.as_dict()
        result_status = 200

    if request.method == 'DELETE':
        log.info(f'DELETE request received for { uid = }')
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


@app.route('/user/<string:uid>', methods=['PUT', 'PATCH'])
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
# @required_token
def user_edit(params: dict, uid: Optional[str] = None, **kwargs):
    log.info(f'PUT/PATCH request received for {uid = } with {params = }')

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


@app.route('/query/<string:table>/<float:value>', methods=['GET'])
@wrap_error
@limiter.limit("100/minute")
# @get_params
# @log_params
# @required_token
def get_classification_data(table: str, value: float):
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
    o2 = db.session().query(db.get_table(table)).all()

    o2_list = [dict(row._mapping) for row in o2]

    return Response(response=json.dumps(o2_list),
                    status=200,
                    mimetype="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
