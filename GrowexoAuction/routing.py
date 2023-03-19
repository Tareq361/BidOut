import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

import Auction.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GrowexoAuction.settings')
django.setup()
asgi_app = get_asgi_application()
application = ProtocolTypeRouter(

    {
        "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            Auction.routing.websocket_urlpatterns
        )
    ),
})
