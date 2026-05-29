import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

_MANAGERS_GROUP = 'alertas_managers'


class AlertaConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer para alertas en tiempo real.
    Cada usuario autenticado escucha su grupo personal.
    Coordinadores y admins escuchan además el grupo de managers.
    """

    async def connect(self):
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            await self.close()
            return

        from users.models.user import User

        self.user_group   = f'alertas_user_{user.pk}'
        self.is_manager   = user.rol in {User.Rol.COORDINADOR, User.Rol.ADMIN}

        await self.channel_layer.group_add(self.user_group, self.channel_name)

        if self.is_manager:
            await self.channel_layer.group_add(_MANAGERS_GROUP, self.channel_name)

        await self.accept()
        await self.send(json.dumps({
            'tipo': 'conexion',
            'mensaje': 'Conectado al sistema de notificaciones.',
        }))

    async def disconnect(self, close_code):
        if hasattr(self, 'user_group'):
            await self.channel_layer.group_discard(
                self.user_group, self.channel_name
            )
        # Solo abandona managers si realmente se unió
        if getattr(self, 'is_manager', False):
            await self.channel_layer.group_discard(
                _MANAGERS_GROUP, self.channel_name
            )

    async def receive(self, text_data):
        """Solo se acepta ping para keepalive."""
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return
        if data.get('tipo') == 'ping':
            await self.send(json.dumps({'tipo': 'pong'}))

    # ── Handlers del channel layer ──────────────────────────────────────────

    async def alerta_nueva(self, event):
        await self.send(json.dumps({
            'tipo':        'alerta_nueva',
            'id':          event['id'],
            'tipo_alerta': event['tipo_alerta'],
            'descripcion': event['descripcion'],
            'fecha':       event['fecha'],
        }))

    async def alerta_conflicto(self, event):
        await self.send(json.dumps({
            'tipo':        'conflicto_horario',
            'descripcion': event['descripcion'],
            'bloque_id':   event['bloque_id'],
            'fecha':       event['fecha'],
        }))