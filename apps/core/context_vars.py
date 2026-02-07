from contextvars import ContextVar
import uuid

# Log context
request_id_var = ContextVar('request_id', default=None)

def get_request_id():
    return request_id_var.get()

def set_request_id(request_id):
    return request_id_var.set(request_id)

def generate_request_id():
    return str(uuid.uuid4())