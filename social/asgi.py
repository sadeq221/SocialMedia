# For more information on this file, see
# https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/

import os

# This is the default but ...
from channels.auth import AuthMiddlewareStack
# We replaced the above by this (read middlewares.py for more info)
from chat.middlewares import TokenAuthMiddleWare

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from chat.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social.settings")

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_application = get_asgi_application()

channels_asgi_application = ProtocolTypeRouter(
    {
        "http": django_asgi_application,
        # AllowedHostsOriginValidator validates only allowed_hosts in settings.py
        "websocket": AllowedHostsOriginValidator(
            # TokenAuthMiddleWare sets user instance using token passed to the connection. 
            TokenAuthMiddleWare(URLRouter(websocket_urlpatterns))
        ),
    }
)
