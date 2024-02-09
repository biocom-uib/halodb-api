import logging
import sys
from flask_log_request_id import RequestIDLogFilter
from flask import request


class RequestEndpointLogFilter(logging.Filter):
    def filter(self, log_record):
        from flask import _app_ctx_stack as stack  # We do not support < Flask 0.9
        if stack.top is not None and request.url_rule:
            log_record.endpoint = str(request.url_rule.rule)
        else:
            log_record.endpoint = "None"

        return log_record


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(levelname)s][%(request_id)s][%(endpoint)s] %(asctime)s - %(message)s"))
handler.addFilter(RequestEndpointLogFilter())
handler.addFilter(RequestIDLogFilter())
log_level = logging.INFO

logger = logging.getLogger('app')
logger.addHandler(handler)
logger.setLevel(log_level)
