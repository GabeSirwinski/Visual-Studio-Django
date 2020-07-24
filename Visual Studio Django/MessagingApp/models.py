from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Message(models.Model):
    senderId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipientId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    dateTime = models.DateTimeField()
    body = models.CharField(max_length=300, default="", blank=True, null=False)
