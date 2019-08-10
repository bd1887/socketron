# chat/routing.py
from django.conf.urls import url
from django.conf import settings


from . import consumers

if settings.RUNNING_DEVSERVER:
    websocket_urlpatterns = [
        url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
    ]
else:
    websocket_urlpatterns = [
        url(r'^socketron/ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
    ]

