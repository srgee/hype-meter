from .context_vars import request_id_var
import uuid
import logging
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger("apps.core")

class ExceptionSafetyNetMiddleware:
    """
    Top-level exception handler to ensure no unhandled exception 
    leaks to the user and is always logged with context.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as exc:
            # We use 'exception' level to automatically capture stack trace
            logger.exception("unhandled_system_exception", extra={
                "path": request.path,
                "method": request.method,
                "is_ajax": request.headers.get('x-requested-with') == 'XMLHttpRequest',
                "user_id": request.user.id if request.user.is_authenticated else "anonymous"
            })

            return self.handle_exception(request, exc)

    def handle_exception(self, request, exc):
        # In development, we might want the standard Django debug page
        if settings.DEBUG:
            raise exc

        # In production, return a clean, branded error response
        message = "An unexpected error occurred. Our team has been notified."
        
        # If it's an HTMX or AJAX request, return a partial or JSON
        if request.headers.get('hx-request'):
            return JsonResponse({"error": message}, status=500)
            
        return JsonResponse({
            "error": "internal_server_error",
            "message": message,
            "request_id": getattr(request, 'request_id', 'unknown') 
        }, status=500)
class RequestContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        rid = request.headers.get('X-Request-ID', str(uuid.uuid4()))
        
        request_id_var.set(rid)
        
        response = self.get_response(request)
        
        response['X-Request-ID'] = rid
        
        return response