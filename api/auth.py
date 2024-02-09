from functools import wraps
from flask import request, abort
from typing import Callable

import firebase_admin
from firebase_admin.auth import ExpiredIdTokenError, RevokedIdTokenError, InvalidIdTokenError, CertificateFetchError, verify_id_token
from google.oauth2 import id_token
from google.auth.transport import requests

from api.constants import FIREBASE_API_KEY, PROJECT_ID


def get_config():
    config = {
        "apiKey": FIREBASE_API_KEY,
        "authDomain": f"{PROJECT_ID}.firebaseapp.com",
        "databaseURL": f"https://{PROJECT_ID}.firebaseio.com",
        "projectId": PROJECT_ID,
        "storageBucket": f"{PROJECT_ID}.appspot.com"
    }
    return config


firebaseapp = firebase_admin.initialize_app(options=get_config())


def verify_token(token):
    if token == '':
        abort(403, "Invalid token")
    try:
        decoded_token = verify_id_token(token, app=firebaseapp, check_revoked=True)
        return decoded_token
    except ExpiredIdTokenError:
        abort(403, "Expired token")
    except RevokedIdTokenError:
        abort(403, "Revoked token")
    except InvalidIdTokenError:
        abort(403, "Invalid token")
    except CertificateFetchError:
        abort(403, "Certificate fetch error")


def required_token(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            abort(401, 'No token provided')
        if not token.startswith('Bearer '):
            abort(401, 'Invalid token type')
        decoded_token = verify_token(token.split(' ')[1])
        return func(*args, **kwargs, **decoded_token)

    return wrapper
