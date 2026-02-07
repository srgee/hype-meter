from .context_vars import request_id_var
import uuid

class RequestContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        rid = request.headers.get('X-Request-ID', str(uuid.uuid4()))
        
        token = request_id_var.set(rid)
        
        response = self.get_response(request)
        
        response['X-Request-ID'] = rid
        
        request_id_var.reset(token)
        return response