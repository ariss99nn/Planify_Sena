import hashlib
from django.utils.cache import patch_cache_control


class ETagMiddleware:
    """
    Agrega ETag a responses GET para que el cliente móvil
    pueda hacer conditional requests y ahorrar ancho de banda.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method == 'GET' and response.status_code == 200:
            etag = hashlib.md5(response.content).hexdigest()
            response['ETag'] = f'"{etag}"'

            if_none_match = request.META.get('HTTP_IF_NONE_MATCH')
            if if_none_match and if_none_match.strip('"') == etag:
                response.status_code = 304
                response.content = b''

        return response