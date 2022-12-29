import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

import Auction.routing

asgi_app = get_asgi_application()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GrowexoAuction.settings')
application = ProtocolTypeRouter(

    {
        "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            Auction.routing.websocket_urlpatterns
        )
    ),
})
