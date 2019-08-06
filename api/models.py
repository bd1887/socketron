from django.db import models
from django.contrib import admin

# Create your models here.
class Twitch_User(models.Model):
    twitch_id = models.IntegerField(primary_key=True, unique=True)

    def __str__(self):
        return str(self.twitch_id)

class ChatResponse(models.Model):
    twitch_user = models.ForeignKey('Twitch_User', on_delete=models.CASCADE)
    input = models.CharField(max_length=255)
    output = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id} - {self.twitch_user} - {self.input} - {self.output}'

admin.site.register(Twitch_User)
admin.site.register(ChatResponse)