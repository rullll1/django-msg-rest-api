from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    author = models.ForeignKey(User, related_name='author', on_delete=models.PROTECT)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.PROTECT)
    subject = models.TextField(max_length=100)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    creation_date = models.DateField()
