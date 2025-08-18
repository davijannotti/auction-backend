
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.auction_group_name = f'auction_{self.auction_id}'

        # Join auction group
        await self.channel_layer.group_add(
            self.auction_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave auction group
        await self.channel_layer.group_discard(
            self.auction_group_name,
            self.channel_name
        )

    # This function is called when the backend (e.g., Celery task) sends a message
    async def auction_ended(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'auction.ended',
            'message': event['message']
        }))
