from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets, status
from rest_framework.views import  APIView
from .serializers import CreateMessageSerializer, ReadMessageSerializer
from .models import Message
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class MessageList(APIView):
    """
    A view to handle the get messages endpoints.
    Can return all messages of authenticated user or all unread messages of authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        if request.user.id != pk:  # trying to access messages of another user => redirecting
            pk = request.user.id

        url_splited  = request.get_full_path().split('/')
        if url_splited[-1] == 'unread':  # get all unread messages
            messages = Message.objects.filter(receiver=pk, is_read=False)
        else:
            messages = Message.objects.filter(receiver=pk)
        serializer = ReadMessageSerializer(messages, many=True)
        return Response(serializer.data)


class CreateDeleteMessage(APIView):
    """
    A view to handle creating messages or deleting messages
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if str(request.user.id) != request.data['author']:
            return Response({"error": "Trying to send message on behalf of another user"}, status=status.HTTP_403_FORBIDDEN)
        serializer = CreateMessageSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, msg_id, format=None):
        try:
            msg = Message.objects.get(pk=msg_id)
        except Message.DoesNotExist:
            return Response({"error": "Message does not exist"}, status.HTTP_404_NOT_FOUND)
        if request.user == msg.author or request.user == msg.receiver:
            msg.delete()
            return Response({'Success: Message was deleted!'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Error": "Trying to delete not your message"},
                            status=status.HTTP_403_FORBIDDEN)


class ReadMessage(APIView):
    """
    A view to handle the reading first unread message in queue.
    after finding the message changing the status of is_read from False to True.
    Returning the message after changing the status
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id):
        msg = Message.objects.filter(receiver=user_id, is_read=False).order_by('creation_date').first()

        if msg:
            msg.is_read = True
            msg.save()

            serializer = ReadMessageSerializer(msg)
            return Response(serializer.data)
        else:
            return Response({"Detail": "You have read all your massages"}, status=status.HTTP_204_NO_CONTENT)
