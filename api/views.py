from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated
from rest_framework import status
from api.models import Twitch_User, ChatResponse
from .serializers import ChatResponseSerializer
from api.utils import verify_and_decode_jwt
from django.conf import settings
import requests
import json

# Create your views here.
def index(request):
    return JsonResponse({'message': 'API Route is working!'})

# Path which Twitch redirects to from their authentication page
def oauth_redirect(request):
    # Retrieve request token from parameters
    request_token = request.GET.get('code')
    
    # Request user's info from Twitch
    redirect_uri = 'http://localhost:3000/oauth/redirect' if settings.RUNNING_DEVSERVER else 'https://www.imugi.io/oauth/redirect'
    oauth_url = f'https://id.twitch.tv/oauth2/token?client_id={settings.CLIENT_ID}&client_secret={settings.CLIENT_SECRET}&code={request_token}&grant_type=authorization_code&redirect_uri={redirect_uri}'
    r = requests.post(oauth_url)
    
    if r.status_code == 200:
        # retrieve ID Token from response
        id_token = json.loads(r.content)['id_token']

        try:
            decoded = verify_and_decode_jwt(id_token)
            username = decoded['preferred_username']
            twitch_id = decoded['sub']
            twitch_user, created = Twitch_User.objects.get_or_create(twitch_id=twitch_id)
            preferred_username = decoded['preferred_username']
            expiry = decoded['exp']
            return JsonResponse({'username': username, 'twitch_id': twitch_id, 'expiry': expiry, 'id_token': id_token})

        except:
            # TODO: Render an authentication error here instead
            return JsonResponse({'message:': r.text})

    else:
        # TODO: Render an authentication error here instead
        return JsonResponse({'message:': r.text})

class ChatResponseViewSet(ViewSet):

    def list(self, request):
        try:
            twitch_id = self.id_from_token(request)
        except:
            raise NotAuthenticated()
        queryset = ChatResponse.objects.filter(twitch_user=twitch_id)
        if not queryset:
            raise NotFound()
        serializer = ChatResponseSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        twitch_id = self.id_from_token(request)
        queryset = ChatResponse.objects.filter(twitch_user=twitch_id)
        if not queryset:
            raise NotFound()
        chat_response = get_object_or_404(queryset, pk=pk)
        serializer = ChatResponseSerializer(chat_response)
        return Response(serializer.data)

    def create(self, request):
        twitch_id = self.id_from_token(request)
        twitch_user = Twitch_User.objects.get(pk=twitch_id)
        input = request.data['input']
        output = request.data['output']
        serializer = ChatResponseSerializer(data={'input': input, 'output': output, 'twitch_user': twitch_user})
        print(serializer.is_valid())
        if serializer.is_valid():
            chat_response = ChatResponse(input=input, output=output, twitch_user=twitch_user)
            chat_response.save()
        return Response(serializer.data)

    def delete(self, request, pk=None):
        twitch_id = self.id_from_token(request)
        queryset = ChatResponse.objects.filter(twitch_user=twitch_id)
        chat_response = get_object_or_404(queryset, pk=pk)
        chat_response.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def id_from_token(self, request):
        token = self.request.COOKIES.get('token')
        decoded = verify_and_decode_jwt(token)
        twitch_id = decoded['sub']
        return twitch_id