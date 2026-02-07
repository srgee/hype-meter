from contextvars import ContextVar

# Log context
request_id_var = ContextVar('request_id', default=None)

def get_request_id():
    return request_id_var.get()