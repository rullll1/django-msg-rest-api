from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('author', 'receiver', 'subject', 'content', 'creation_date')


class ReadMessageSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    receiver = UserSerializer()
    class Meta:
        model = Message
        fields = ('author', 'receiver', 'subject', 'content', 'creation_date')
