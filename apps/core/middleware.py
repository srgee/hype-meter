from .context_vars import request_id_var
import uuid

class RequestContextMiddleware:
    def __init__(self, get_response):
        """
        Constructor for RequestContextMiddleware.
        
        Args:
            get_response (function): The get_response function from the Django middleware chain.
        """
        self.get_response = get_response

    def __call__(self, request):
        # 1. Generamos un ID único para ESTA petición
        # Si viene de un balanceador (ej. Nginx), podrías usar su ID
        rid = request.headers.get('X-Request-ID', str(uuid.uuid4()))
        
        # 2. Lo guardamos en el contexto
        token = request_id_var.set(rid)
        
        response = self.get_response(request)
        
        # 3. Lo añadimos a la respuesta para facilitar el debug desde el navegador
        response['X-Request-ID'] = rid
        
        # 4. Limpiamos al salir
        request_id_var.reset(token)
        return response