from flask import request
from functools import wraps
from schema import SchemaError
from werkzeug.exceptions import HTTPException

from api import log


def error(message: str, status_code: int, **kwargs):
    return dict(message=message, status="error", **kwargs), status_code


def ok_message(**kwargs):
    return dict(status="ok", **kwargs), int(200)


def get_params(func):
    @wraps(func)
    def run(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'PATCH']:
            params = request.json
        else:
            params = dict(request.args)
        return func(params, *args, **kwargs)

    return run


def log_params(func):
    @wraps(func)
    def run(params, *args, **kwargs):
        log.debug(f"{params = }")
        return func(params, *args, **kwargs)

    return run


def wrap_error(func):
    @wraps(func)
    def run(*args, **kwargs):
        def inner():
            try:
                return func(*args, **kwargs)
            except AbortError as e:
                log.exception(e)
                return error(e.message, e.status_code, **e.extra)
            except HTTPException as e:
                if e.code == 200:
                    extra = getattr(e, "extra", {}) or {}
                    return ok_message(message=e.description, **extra)
                log.exception(e)
                return error(e.description, e.code)
            except SchemaError as e:
                log.exception(e)
                return error(str(e), 400)
            except Exception as e:
                log.exception(e)
                return error("Unknown error", 500)
        resp = inner()
        return resp

    return run


class AbortOk(HTTPException):
    def __init__(self, description, extra=None) -> None:
        self.code = 200
        self.description = description
        self.extra = extra


class AbortError(HTTPException):
    def __init__(self, status_code: int, message: str, **kwargs) -> None:
        self.status_code = status_code
        self.message = message
        self.extra = kwargs
