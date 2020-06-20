from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    author = models.ForeignKey(User, related_name='created_messages', on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.DO_NOTHING)
    subject = models.TextField(max_length=100)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    creation_date = models.DateField(auto_now=True)
