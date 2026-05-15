import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'dashboard'

        # Suscribirse al grupo dashboard
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'tipo': 'conectado',
            'mensaje': 'Conexión WebSocket establecida exitosamente'
        }))

    async def disconnect(self, close_code):
        # Desuscribirse del grupo
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['tipo'] == 'ping':
            await self.send(text_data=json.dumps({
                'tipo': 'pong'
            }))

    # Método que recibe eventos desde el grupo (llamado desde Django signals)
    async def dashboard_actualizar(self, event):
        await self.send(text_data=json.dumps({
            'tipo': 'actualizacion',
            'mensaje': event['mensaje'],
            'datos': event.get('datos', {})
        }))
