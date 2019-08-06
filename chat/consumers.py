from channels.generic.websocket import WebsocketConsumer
import json
import twitch
from django.conf import settings
from chat.bot import Bot
from api.utils import verify_and_decode_jwt
from api.models import Twitch_User, ChatResponse

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # TODO: Find a more sensible authentication strategy using twitch 'sub' id perhaps
        decoded = verify_and_decode_jwt(self.scope['cookies']['token'])
        if decoded['preferred_username'] == self.scope['url_route']['kwargs']['room_name']:
            # Get user
            self.user_id = decoded['sub']
            self.twitch_user = Twitch_User.objects.get(pk=self.user_id)
            self.chat_responses = ChatResponse.objects.filter(twitch_user=self.twitch_user)

            # Get channel name from route
            self.room_name = self.scope['url_route']['kwargs']['room_name']

            # Accept connection
            self.accept()

            # Instantiate Twitch chat
            self.twitch_chat = twitch.Chat(channel=self.room_name, nickname=settings.BOT_USERNAME, oauth=settings.OAUTH_TOKEN)

            # Subscribe to Twtich chat and relay all messages to socket connection
            self.sub = self.twitch_chat.subscribe(lambda msg: self.message(msg))
            self.send(text_data=json.dumps({
                'message': f'Connected to {self.room_name}!'
            }))

            # Instantiate chat bot
            self.bot = Bot(self.chat_responses)

    def disconnect(self, close_code):
        self.close()
        pass

    def message(self, msg):
        # Relay message from Twitch chat to dashboard chat
        self.send(text_data=json.dumps({
            'message': msg.text
        }))

        # Send message to bot and get response
        response = self.bot.get_response(msg)
        if response: self.twitch_chat.send(response)

    def receive(self, text_data):
        data = json.loads(text_data)
        
        if data.get('update'):
            self.update_responses()

        elif data.get('message'):
            message = text_data_json['message']
            self.send(text_data=json.dumps({
                'message': message
            }))

    def update_responses(self):
        self.chat_responses = ChatResponse.objects.filter(twitch_user=self.twitch_user)
        self.bot = Bot(self.chat_responses)