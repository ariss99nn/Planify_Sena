from django.urls import path
from notificaciones.consumers import AlertaConsumer

websocket_urlpatterns = [
    path('ws/alertas/', AlertaConsumer.as_asgi()),
]