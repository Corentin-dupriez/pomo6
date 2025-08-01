from django.urls import re_path
from . import consumers

consumer = consumers.ChatConsumer.as_asgi()
print(f'consumer {consumer}')

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<thread_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]