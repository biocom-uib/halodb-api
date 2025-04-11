import datetime
import json
from functools import wraps
from flask import request, abort, Response, jsonify
from typing import Callable


from google.oauth2 import id_token
from google.auth.transport import requests

import jwt

from api.config import CREDENTIALS_FILE
from api.main import app
from api.utils import serialize_datetime


def get_credentials(field):
    """
    Extract from credentials file the credential value indicated by the parameter
    :param field: the credential desired
    :return: the value if exists
    """
    with open(CREDENTIALS_FILE, "r") as fin:
        credentials = json.load(fin)
    return credentials[field]

def generate_valid_token(uid):
    new_token = jwt.encode(
        {
            'uid': uid,
            'exp':   datetime.datetime.now(datetime.UTC)
                   + datetime.timedelta(seconds=app.config['SESSION_TIME_IN_SECONDS'])  # New token valid for 30 minutes
        },
        get_credentials('private_key'),
        algorithm='HS256'
    )
    return new_token

def verify_token(token, abort_if_expired=True):
    if token == '':
        abort(403, "Invalid token")
    try:
        decoded_token = jwt.decode(token, get_credentials('private_key'), algorithms=['HS256'])
        time_remaining = time_elapsed(decoded_token['exp'])
        if time_remaining < 0 and abort_if_expired:
            abort(404, "Expired token")
        return decoded_token
    except jwt.exceptions.ExpiredSignatureError:
        abort(403, "Expired token")
    except jwt.exceptions.InvalidTokenError:
        abort(403, "Invalid token")
    except jwt.exceptions.DecodeError:
        abort(404, "Validation failed")
    except jwt.exceptions.InvalidKeyError:
        abort(403, "Invalid key")
    except jwt.exceptions.InvalidSignatureError:
        abort(403, "Certificate fetch error")


def time_elapsed(original_time):
    exp_time = datetime.datetime.fromtimestamp(original_time, tz=datetime.timezone.utc)
    return (exp_time - datetime.datetime.now(datetime.UTC)).total_seconds()

def update_token(decoded_token, current_token):
    # Renew the expiration time if the token expiration time is near.
    time_remaining = time_elapsed(decoded_token['exp'])

    # If the expiration time is less than 5 minutes from now, generate a new token
    if time_remaining < app.config['SESSION_MIN_TIME_IN_SECONDS'] :
        token = generate_valid_token(decoded_token['user_id'])
    else:
        token = current_token

    return token


def required_token(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            abort(401, 'No token provided')
        if not token.startswith('Bearer '):
            abort(401, 'Invalid token type')
        token = token.split(' ')[1]
        decoded_token = verify_token(token, True)

        payload, status = func(*args, **kwargs, **decoded_token)

        message = {'message':payload, 'token':update_token(decoded_token, token)}

        response = Response(response=json.dumps(message, default=serialize_datetime),
                            status=status,
                            mimetype="application/json")
        return response

    return wrapper


def not_required_token(func: Callable) -> Callable:
    @wraps(func)
    def filter_auth(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token is not None:
            if not token.startswith('Bearer '):
                abort(403, 'Invalid token type')
            token = token.split(' ')[1]
            decoded_token = verify_token(token, False)
        else:
            decoded_token = {'uid': None}

        payload, status = func(*args, **kwargs, **decoded_token)

        # Test is payload is already a Response object (that means it was already processed)
        # and the status is 200, then send the payload as is
        if type(payload) is Response and status == 200:
            return payload

        if token is not None:
            message = {'message':payload, 'token':update_token(decoded_token, token)}
        else:
            message = {'message':payload}

        response = Response(response=json.dumps(message, default=serialize_datetime),
                            status=status,
                            mimetype="application/json")
        return response

    return filter_auth