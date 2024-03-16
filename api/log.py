import logging
from flask_log_request_id import RequestIDLogFilter
from flask import has_request_context, request


class RequestEndpointLogFilter(logging.Filter):
    def filter(self, log_record):
        if has_request_context() and request.url_rule:
            log_record.endpoint = str(request.url_rule.rule)
        else:
            log_record.endpoint = "None"

        return log_record

_logger = None

def setup_logger(app, gunicorn: bool):
    global _logger
    _logger = app.logger

    if gunicorn:
        gunicorn_logger = logging.getLogger('gunicorn.error')
        _logger.setLevel(gunicorn_logger.level)
    else:
        _logger.setLevel(logging.INFO)

    for handler in _logger.handlers:
        handler.addFilter(RequestEndpointLogFilter())
        # handler.addFilter(RequestIDLogFilter())
        # handler.setFormatter(logging.Formatter("[%(levelname)s][%(request_id)s][%(endpoint)s] %(asctime)s - %(message)s"))
        handler.setFormatter(logging.Formatter("[%(levelname)s][%(endpoint)s] %(asctime)s - %(message)s"))

    return _logger

def get_logger():
    return _logger

def debug(msg, *args, **kwargs):
    return _logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    return _logger.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    return _logger.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    return _logger.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    return _logger.critical(msg, *args, **kwargs)

def log(msg, *args, **kwargs):
    return _logger.log(msg, *args, **kwargs)

def exception(msg, *args, **kwargs):
    return _logger.exception(msg, *args, **kwargs)
