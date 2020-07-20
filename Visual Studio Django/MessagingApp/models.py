from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Message(models.Model):
    recipientId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    senderId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    chainId = models.IntegerField()
    dateTime = models.DateTimeField()
    subject = models.CharField(max_length=60, default="", blank=True)
    body = models.CharField(max_length=300, default="", blank=True, null=False)