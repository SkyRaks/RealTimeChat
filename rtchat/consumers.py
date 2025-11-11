import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync

from .models import *


class ChatroomConsumer(WebsocketConsumer):
    # this all is still sync
    # this is like view function
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)

        # adding ability for other users to see messages
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )

        self.accept()

    # close the channel layer eg user closed the page so he left
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        message = GroupMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom
        )

        event = {
            'type': 'message_handler',
            'message_id': message.id
        }

        # this will replace send func because we send to everyone in the group
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,
            event
        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
        }

        # similar to render in view
        html = render_to_string('rtchat/partials/chat_message_partial.html', context=context)
        # this is sync send method
        self.send(text_data=html)
