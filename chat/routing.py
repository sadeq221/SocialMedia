from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # (?P<room_name>\w+): This is a capturing group that captures the room name from the URL.
    # The ?P<room_name> part indicates that the captured group should be named room_name.
    re_path(r"ws/chatrooms/$", consumers.ChatConsumer.as_asgi()),
]