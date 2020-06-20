from django.urls import path
from .views import *

urlpatterns = [
    path('v1/messages/create', CreateDeleteMessage.as_view()),
    path('v1/messages/<int:pk>', MessageList.as_view()),
    path('v1/messages/<int:pk>/unread', MessageList.as_view()),
    path('v1/messages/delete/<int:msg_id>', CreateDeleteMessage.as_view()),
    path('v1/messages/read_message/<int:user_id>', ReadMessage.as_view()),
    path('v2/messages/<str:user_name>/', CreateReadMessages.as_view()),
    path('v2/messages/<str:user_name>/unread', CreateReadMessages.as_view()),
    path('v2/messages/create/', CreateReadMessages.as_view()),
    path('v2/messages/delete/<int:msg_id>', DeleteMessage.as_view()),
    path('v2/messages/<str:user_name>/read_message', ReadSingleMessage.as_view()),
]
