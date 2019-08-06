from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import index, oauth_redirect, ChatResponseViewSet

router = DefaultRouter()

urlpatterns = [
    path('', index),
    path("oauth/redirect/", oauth_redirect),
]

router.register('chat-responses', ChatResponseViewSet, basename='chat-response')
urlpatterns += router.urls