import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.middleware import BaseMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django_asgi_app = get_asgi_application()


class TokenAuthMiddleware(BaseMiddleware):
    """Autentica al usuario desde el JWT en el query param ?token=<jwt>"""

    async def __call__(self, scope, receive, send):
        from urllib.parse import parse_qs
        from django.contrib.auth.models import AnonymousUser

        query_string = scope.get('query_string', b'').decode()
        params = parse_qs(query_string)
        token = params.get('token', [None])[0]

        if token:
            try:
                from rest_framework_simplejwt.tokens import AccessToken
                from django.contrib.auth import get_user_model
                User = get_user_model()
                access_token = AccessToken(token)
                user = await User.objects.aget(pk=access_token['user_id'])
                scope['user'] = user
            except Exception:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)


from notificaciones.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': TokenAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})