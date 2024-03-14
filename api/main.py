import json
import os

from typing import Optional

from flask import Flask, Response, send_from_directory
from flask_cors import CORS
from flask_log_request_id import RequestID
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from api.log import logger
from api.auth import required_token

from api.decorators import wrap_error, get_params, log_params


from api.db.db import get_session, db, SQLALCHEMY_DATABASE_URI


app = Flask(__name__)
CORS(app)
RequestID(app)
limiter = Limiter(get_remote_address, app=app)


app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['static_folder'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'static')

db.init_app(app)


@app.route("/")
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def dummy(params: dict, email: Optional[str] = None, **kwargs):
    logger.info(f"Request received for { email = } with { params = }")
    return {"message": "OK"}


@app.route('/query/sample/<id>/', methods=['GET'])
def get_sample(id=None):
    return send_from_directory(app.config['static_folder'], 'sample42.json')


@app.route('/query/<string:table>/')
def get_table_data(table=None):
    o2 = get_session().query(db.metadata.tables[table]).all()

    o2_list = [dict(row._mapping) for row in o2]

    return Response(response=json.dumps(o2_list),
                    status=200,
                    mimetype="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
