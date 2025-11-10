from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class ChatGroup(models.Model):
    # table for chatrooms
    group_name = models.CharField(max_length=128, unique=True, blank=True)

    def __str__(self):
        return self.group_name

class GroupMessage(models.Model):
    # connecting with mian chat group model
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300) #length of the message
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.body}"

    class Meta:
        ordering = ['-created']

