from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.Login, name="LoginPage"),
    path('register/', views.Register, name="RegisterPage"),
    path('messages/', views.MessagesView, name="MessagesPage"),
    path('messages/chat/<str:username>', views.ChatView, name="ChatPage")
]