from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TransactionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("transactions", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("transactions", self.channel_name)

    async def receive(self, text_data):
        # Optional: handle messages from the client
        pass

    async def transaction_update(self, event):
        # Send a message to the client
        await self.send(text_data=json.dumps({
            "type": "update",
        }))
