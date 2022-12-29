# chat/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/auction-details/(?P<p_id>[0-9]+)/$', consumers.LiveBiddingConsumer.as_asgi()),
]

