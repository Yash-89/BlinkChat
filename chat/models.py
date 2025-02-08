from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

class Room(models.Model):
    name = models.CharField(max_length=1000)
class Message(models.Model):
    msg = models.CharField(max_length=1000000)
    user = models.CharField(max_length=1000)
    room = models.CharField(max_length=1000)
    date = models.DateTimeField(default=datetime.now, blank=True)
class CustomUser(AbstractUser):
    dob = models.DateField(null=True, blank=True)