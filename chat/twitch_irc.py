import socket
from django.conf import settings
from threading import Thread
import re

class TwitchIrc:
    def __init__(self, channel):
        self.server = 'irc.chat.twitch.tv'
        self.port = 6667
        self.nickname = settings.BOT_USERNAME
        self.token = settings.OAUTH_TOKEN
        self.channel = f'#{channel}'
        
    def send(self, msg):
        msg = f"PRIVMSG {self.channel} :{msg}\r\n".encode('utf-8')
        # msg = f"{msg}".encode('utf-8')
        print(repr(msg))
        self.socket.send(msg)

    def listen(self, callback):
        self.socket = socket.socket()
        self.socket.connect((self.server, self.port))
        self.socket.send(f"PASS {self.token}\r\n".encode('utf-8'))
        self.socket.send(f"NICK {self.nickname}\r\n".encode('utf-8'))
        self.socket.send(f"JOIN {self.channel}\r\n".encode('utf-8'))

        self.thread = Thread(target = self._threaded_function, args=(callback,))
        self.thread.start()

    def _parse_message(self, resp):
        if resp.startswith(':tmi.twitch.tv'):
            print('Official Babble')
            return ''
        else:
            try:
                username, channel, message = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', resp).groups()
                message = message[:-1]
                return message
            except:
                print(resp)

    def _threaded_function(self, args):
        callback = args
        while True:
            resp = self.socket.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                self.socket.send("PONG\n".encode('utf-8'))
                
            if resp:
                msg = self._parse_message(resp)
                callback(msg)