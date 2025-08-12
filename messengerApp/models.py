from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Chat(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    speaking_partner = models.CharField(max_length=100)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    content = models.CharField(max_length=100)
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)

