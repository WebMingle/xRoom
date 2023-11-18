from django.db import models

class Room(models.Model):
    room_id = models.CharField(max_length=20, unique=True)
    max_users = models.IntegerField(default=2)
    password = models.CharField(max_length=20)
    expiration_time = models.DateTimeField()

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

