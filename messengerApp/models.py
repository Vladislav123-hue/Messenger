from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class BlockedUsers(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='blockedUsers')
    username = models.CharField(max_length=100, null=True, blank=True)


class Chat(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='chats')
    speaking_partner = models.CharField(max_length=100, null=True, blank=True)
    speaking_partner_username = models.CharField(
        max_length=100, null=True, blank=True)


class Message(models.Model):
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name='messages')
    content = models.CharField(max_length=100, null=True, blank=True)
    sender = models.CharField(max_length=100, null=True, blank=True)
    receiver = models.CharField(max_length=100, null=True, blank=True)
    his_message_id = models.IntegerField(null=True, blank=True)
