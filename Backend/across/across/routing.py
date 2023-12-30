from django.urls import re_path

from polls import socket_consumer

websocket_urlpatterns = [
    re_path(r"ws/updates", socket_consumer.Consumer.as_asgi()),
]