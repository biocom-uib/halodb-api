from typing import Optional
from flask import Flask
from flask_cors import CORS
from flask_log_request_id import RequestID
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from api.logging import logger
from api.auth import required_token

from api.decorators import wrap_error, get_params, log_params

app = Flask(__name__)
CORS(app)
RequestID(app)
limiter = Limiter(get_remote_address, app=app)


@app.route("/")
@wrap_error
@limiter.limit("100/minute")
@get_params
@log_params
@required_token
def dummy(params: dict, email: Optional[str] = None, **kwargs):
    logger.info(f"Request received for { email = } with { params = }")
    return {"message": "OK"}


if __name__ == "__main__":
    app.run(host="0.0.0.0")
