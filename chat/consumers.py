import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Thread, Message
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.other_user = self.scope['url_route']['kwargs']['other_user']

        self.other_user = await self.get_user(self.other_user)
        if not self.user.is_authenticated or not self.other_user:
            await self.close()
            return

        self.chat = await self.get_or_create_chat(self.user, self.other_user)
        self.thread_id = self.chat.id
        self.room_name = f'chat_{self.chat.id}'

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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['content']
        sender_id = self.scope['user'].id

        await self.save_message(sender_id, content)

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'sender_id': sender_id,
                'content': content
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'sender_id': self.scope['user'].username,
            'content': event['content']
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_or_create_chat(self, user, other_user):
        chat = Thread.objects.filter(participants=user).filter(participants=other_user).first()
        if chat:
            return chat

        chat = Thread.objects.create()
        chat.participants.set([user, other_user])
        return chat

    @sync_to_async
    def save_message(self, sender_id, content):
        thread = Thread.objects.get(pk=self.thread_id)
        sender = User.objects.get(pk=sender_id)
        Message.objects.create(thread=thread, sender=sender, content=content)