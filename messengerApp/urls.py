from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.Login, name="LoginPage"),
    path('register/', views.Register, name="RegisterPage"),
    path('messages/', views.MessagesView, name="MessagesPage"),
    path('messages/chat/<str:username>', views.ChatView, name="ChatPage"),
    path('messages/chat/delete_message/<int:message_id>/<str:username>/<int:his_message_id>',
         views.MessageDelete, name="DeleteMessage"),
    path('messages/chat/delete_message_confirm/<int:message_id>/<str:username>/<int:his_message_id>',
         views.Message_delete_confirm, name="DeleteMessageConfirm"),
    path('messages/chat/edit_message/<int:message_id>/<str:username>/<int:his_message_id>',
         views.MessageEdit, name="EditMessage"),
    path('messages/chat/edit_message_confirm/<int:message_id>/<str:username>/<int:his_message_id>',
         views.MessageEditConfirm, name="EditConfirm"),
    path('messages/chat/delete_chat/<int:chat_id>',
         views.DeleteChat, name="DeleteChat"),
    path('messages/chat/delete_chat_confirm/<int:chat_id>',
         views.DeleteChatConfirm, name="DeleteChatConfirm"),
    path("logout/", views.logout_view, name="logout"),
    path("block/<str:username>", views.BlockUser, name="blockUser"),
    path("unblock/<str:username>", views.UnblockUser, name="unblockUser")
]
