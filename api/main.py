import json
import os
import random

from typing import Optional

from flask import Flask, Response, send_from_directory, jsonify
from flask_cors import CORS
from flask_log_request_id import RequestID
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from api import log
from api.auth import required_token

from api.decorators import wrap_error, get_params, log_params


from api.db.db import SQLALCHEMY_DATABASE_URI, wait_for_connection_and_create_instance


app = Flask(__name__)
CORS(app)
RequestID(app)
limiter = Limiter(get_remote_address, app=app)

log.setup_logger(app, gunicorn = __name__ != '__main__')

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['static_folder'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'static')

log.info('Waiting for the database to be ready')
db = wait_for_connection_and_create_instance(wait_time = 5, attempts = -1)
log.info('The database is ready')

db.init_app(app)


@app.route("/")
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def dummy(params: dict, email: Optional[str] = None, **kwargs):
    log.info(f"Request received for { email = } with { params = }")
    return {"message": "OK"}


@app.route('/upload/sample/', methods=['POST'])
def upload_sample():
    return jsonify({"message": "OK"})


@app.route('/query/sample_list/', methods=['GET'])
def get_sample_list():
    random.seed()
    start = 5
    end = 11 + random.randint(0, 10)
    indexes = list(range(start, end))
    random.shuffle(indexes)

    samples = [{"id": idx, "name": "Sample {}".format(idx)} for idx in indexes]

    return Response(json.dumps(samples), mimetype="application/json")

@app.route('/query/sample/<id>/', methods=['GET'])
def get_sample(id=None):
    log.info(f'Requested sample with {id = }')
    return send_from_directory(app.config['static_folder'], 'sample42.json')


@app.route('/query/<string:table>/')
def get_table_data(table=None):
    o2 = db.get_session().query(db.metadata.tables[table]).all()

    o2_list = [dict(row._mapping) for row in o2]

    return Response(response=json.dumps(o2_list),
                    status=200,
                    mimetype="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
