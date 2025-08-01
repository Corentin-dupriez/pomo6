import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Thread, Message
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.chat = await self.get_chat(self.thread_id)
        self.room_name = f'chat_{self.thread_id}'

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

        has_messages = await sync_to_async(self.chat.messages.exists)()

        if not has_messages:
            await sync_to_async(self.chat.delete)()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['content']
        sender_id = self.scope['user'].id
        sender = await self.get_user(sender_id)
        sender_name = sender.username

        await self.save_message(sender_id, content)

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'sender_id': sender_id,
                'sender_name': sender_name,
                'content': content
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'content': event['content']
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.filter(pk=user_id).first()
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_chat(self, chat_id):
        return Thread.objects.filter(pk=chat_id).first()

    @sync_to_async
    def save_message(self, sender_id, content):
        thread = Thread.objects.get(pk=self.thread_id)
        sender = User.objects.get(pk=sender_id)
        Message.objects.create(thread=thread, sender=sender, content=content)