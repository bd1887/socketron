import socket
from django.conf import settings
from threading import Thread
import re

class TwitchIrc:
    def __init__(self, channel):
        # Credentials and stuff
        self.server = 'irc.chat.twitch.tv'
        self.port = 6667
        self.nickname = settings.BOT_USERNAME
        self.token = settings.OAUTH_TOKEN
        self.channel = f'#{channel}'
        
    def send(self, msg):
        msg = f"PRIVMSG {self.channel} :{msg}\r\n".encode('utf-8')
        self.socket.send(msg)

    def listen(self, callback):
        # instantiate socket
        self.socket = socket.socket()

        # Connect to Twitch
        self.socket.connect((self.server, self.port))

        # Login into user's channel with Socketron bot credentials
        self.socket.send(f"PASS {self.token}\r\n".encode('utf-8'))
        self.socket.send(f"NICK {self.nickname}\r\n".encode('utf-8'))
        self.socket.send(f"JOIN {self.channel}\r\n".encode('utf-8'))

        # Start a thread to listen to chat messages, pass in the callback function
        self.thread = Thread(target = self._threaded_function, args=(callback,))
        self.thread.start()

    def _parse_message(self, resp):
        # Ignore system messages
        if resp.startswith(':tmi.twitch.tv'):
            pass
        else:
            # Exctract username, channel, and message
            try:
                username, channel, message = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', resp).groups()
                message = message[:-1]
                return message
            except:
                # Just in case the regex fails
                pass

    def _threaded_function(self, args):
        callback = args # Get callback function from args
        while True:

            # Listen for new messages from socket
            resp = self.socket.recv(2048).decode('utf-8')

            # Respond to PINGs from Twitch
            if resp.startswith('PING'):
                self.socket.send("PONG\n".encode('utf-8'))
                
            # Pass the parsed message back to the callback function
            # to be further handled in consumers.py
            if resp:
                msg = self._parse_message(resp)
                callback(msg)