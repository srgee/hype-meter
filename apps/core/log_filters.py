import logging
from .context_vars import get_request_id

class RequestContextFilter(logging.Filter):
    def filter(self, record):
        # Inject request_id in the log record if it exists
        record.request_id = get_request_id()
        return True