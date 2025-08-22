from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile, Chat, Message
from django.contrib.auth.decorators import login_required

# Create your views here.


def Login(request):
    if request.method == "POST":
        username = request.POST.get('Username')
        password = request.POST.get('Password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('MessagesPage')
        else:
            error = "False login or password"
            return render(request, 'Login.html', {'error': error})

    return render(request, 'Login.html')


def Register(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get('Username')
        email = request.POST.get('Email')
        password1 = request.POST.get('Password1')
        password2 = request.POST.get('Password2')
        first_name = request.POST.get('First_name')
        last_name = request.POST.get('Last_name')

        if password1 != password2:
            error = "Passwords not equal"
            return render(request, 'register.html', {'error': error})

        # Проверка, что пользователь с таким именем ещё не существует
        if User.objects.filter(username=username).exists():
            error = "Такой логин уже есть"
            return render(request, 'register.html', {'error': error})

        # Создаём пользователя
        user = User.objects.create_user(
            username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
        Profile.objects.create(user=user)
        return redirect('LoginPage')  # После регистрации — на логин

    return render(request, 'Register.html')


@login_required
def MessagesView(request):
    my_profile = Profile.objects.get(user__username=request.user.username)
    my_chats = my_profile.chats.all()
    if request.method == "POST":
        query = request.POST.get('user')
        if query:
            results = User.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            ).exclude(username=request.user.username)
    else:
        results = []
    return render(request, 'Messages.html', {'results': results, 'my_chats': my_chats})


@login_required
def ChatView(request, username):
    speaking_partner_name = User.objects.get(
        username=username).first_name + " " + User.objects.get(username=username).last_name
    my_name = User.objects.get(username=request.user.username).first_name + \
        " " + User.objects.get(username=request.user.username).last_name
    try:
        my_profile = Profile.objects.get(user__username=request.user.username)
        ourChat, _ = Chat.objects.get_or_create(
            profile=my_profile,
            speaking_partner=speaking_partner_name,
            speaking_partner_username=username
        )
        messages = ourChat.messages.all()
    except Chat.DoesNotExist:
        ourChat = []
        messages = []
    if request.method == "POST":
        query = request.POST.get('text')
        if query:
            my_profile = Profile.objects.get(
                user__username=request.user.username)
            ourChat, _ = Chat.objects.get_or_create(
                profile=my_profile,
                speaking_partner=speaking_partner_name,
                speaking_partner_username=username
            )
            Message.objects.get_or_create(
                chat=ourChat,
                content=query,
                sender=request.user.username,
                receiver=username
            )
            his_profile = Profile.objects.get(user__username=username)
            his_chat, _ = Chat.objects.get_or_create(
                profile=his_profile,
                speaking_partner=my_name,
                speaking_partner_username=request.user.username
            )
            Message.objects.get_or_create(
                chat=his_chat,
                content=query,
                sender=request.user.username,
                receiver=username
            )
    return render(request, 'Chat.html', {'speaking_partner_name': speaking_partner_name, 'messages': messages})


@login_required
def MessageDelete(request, message_id, username):
    message = Message.objects.get(id=message_id)
    chat = message.chat
    messages = chat.messages.all()
    speaking_partner_name = chat.speaking_partner
    return render(request, 'DeletePage.html', {
        'messages': messages,
        'speaking_partner_name': speaking_partner_name,
        'message': message,
        'username': username
    })


@login_required
def Message_delete_confirm(request, message_id, username):
    my_message = Message.objects.get(id=message_id)
    my_message.delete()
    return redirect('ChatPage', username=username)
