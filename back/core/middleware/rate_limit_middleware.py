from django.core.cache import cache
from django.http import JsonResponse


class RolBasedRateLimitMiddleware:
    """
    Rate limiting diferenciado por rol.
    Requiere cache configurado (Redis recomendado en producción).
    """
    LIMITES = {
        'ADMINISTRATIVO': 1000,
        'COORDINADOR': 1000,
        'DOCENTE': 500,
        'ESTUDIANTE': 200,
        None: 50,
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        rol = None
        if hasattr(request, 'user') and request.user.is_authenticated:
            rol = getattr(request.user, 'rol', None)

        limite = self.LIMITES.get(rol, 50)
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        key = f'rate_limit:{rol}:{ip}'
        hits = cache.get(key, 0)

        if hits >= limite:
            return JsonResponse(
                {'detail': 'Límite de solicitudes alcanzado. Intenta más tarde.'},
                status=429,
            )

        cache.set(key, hits + 1, timeout=3600)
        return self.get_response(request)