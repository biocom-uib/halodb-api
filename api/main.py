import json
import os
from typing import Optional

from flask import Flask, Response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_log_request_id import RequestID

from api import log
from api.db.db import SQLALCHEMY_DATABASE_URI, DatabaseInstance
from api.decorators import wrap_error, get_params, log_params

# from api.db.models  # Do not import yet, the database must be initialized first


app = Flask(__name__)

CORS(app)
RequestID(app)
limiter = Limiter(get_remote_address, app=app, default_limits = ["100/minute"])

log.setup_logger(app, gunicorn=__name__ != '__main__')

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['static_folder'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'static')

mocked_sample_file = 'sample42.json'

log.info('Waiting for the database to be ready')

db = DatabaseInstance.wait_for_connection_and_create_instance(wait_time=5, attempts=-1)

if db is not None:
    log.info('The database is ready')

    from api.blueprints.user import user_page
    from api.blueprints.group import group_page
    from api.blueprints.project import project_page
    from api.blueprints.sequence import sequence_page
    from api.blueprints.general import general_page

    # limiter.limit("100/minute")(app)
    limiter.limit("100/minute")(user_page)
    limiter.limit("100/minute")(group_page)
    limiter.limit("100/minute")(project_page)
    limiter.limit("100/minute")(sequence_page)
    limiter.limit("100/minute")(general_page)

    app.register_blueprint(user_page)
    app.register_blueprint(group_page)
    app.register_blueprint(project_page)
    app.register_blueprint(sequence_page)
    app.register_blueprint(general_page)

    db.init_app(app)
else:
    log.error('The database could not be initialized')

@app.route("/")
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
# @required_token
def dummy(params: dict, email: Optional[str] = None, **kwargs):
    log.info(f"Request received for { email = } with { params = }")
    return {"message": "OK"}



# ######################################################
# General purposes handling
# ######################################################

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


if __name__ == "__main__":
    app.run(host="0.0.0.0")
