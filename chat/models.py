from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)

class Message(models.Model):
    value = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    room = models.CharField(max_length=100)
    #user = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.CharField(max_length=100)

