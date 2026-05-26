import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class AlertaConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer para alertas en tiempo real.
    Cada usuario autenticado se conecta a su propio grupo personal.
    IsManager se conecta además al grupo 'managers' para alertas globales.
    """

    async def connect(self):
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            await self.close()
            return

        self.user_group = f'alertas_user_{user.pk}'
        await self.channel_layer.group_add(
            self.user_group, self.channel_name
        )

        # IsManager recibe alertas de conflicto del sistema
        from users.models.user import User
        if user.rol in {User.Rol.COORDINADOR, User.Rol.ADMIN}:
            await self.channel_layer.group_add(
                'alertas_managers', self.channel_name
            )

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
        await self.channel_layer.group_discard(
            'alertas_managers', self.channel_name
        )

    async def receive(self, text_data):
        # El cliente solo escucha — no envía mensajes al servidor
        pass

    async def alerta_nueva(self, event):
        """Handler para mensajes del tipo 'alerta.nueva' del channel layer."""
        await self.send(json.dumps({
            'tipo': 'alerta_nueva',
            'id': event['id'],
            'tipo_alerta': event['tipo_alerta'],
            'descripcion': event['descripcion'],
            'fecha': event['fecha'],
        }))

    async def alerta_conflicto(self, event):
        """Handler para conflictos de horario — solo managers."""
        await self.send(json.dumps({
            'tipo': 'conflicto_horario',
            'descripcion': event['descripcion'],
            'bloque_id': event['bloque_id'],
            'fecha': event['fecha'],
        }))