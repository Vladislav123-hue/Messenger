from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile, Chat, Message, BlockedUsers
from django.contrib.auth.decorators import login_required


# Login view
def Login(request):
    if request.method == "POST":   # If form submitted
        username = request.POST.get('Username')
        password = request.POST.get('Password')

        # Authenticate user with Django’s built-in system
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)   # Log the user in
            return redirect('MessagesPage')   # Redirect to messages
        else:
            # If authentication fails, return error
            error = "False login or password"
            return render(request, 'Login.html', {'error': error})

    # If GET request → show login page
    return render(request, 'Login.html')


# Register view
def Register(request):
    if request.method == "POST":
        print(request.POST)  # Debugging – shows submitted data in console
        username = request.POST.get('Username')
        email = request.POST.get('Email')
        password1 = request.POST.get('Password1')
        password2 = request.POST.get('Password2')
        first_name = request.POST.get('First_name')
        last_name = request.POST.get('Last_name')

        # Check if passwords match
        if password1 != password2:
            error = "Passwords not equal"
            return render(request, 'register.html', {'error': error})

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            error = "Такой логин уже есть"  # "This username already exists"
            return render(request, 'register.html', {'error': error})

        # Create new user + related Profile
        user = User.objects.create_user(
            username=username, email=email, password=password1,
            first_name=first_name, last_name=last_name
        )
        Profile.objects.create(user=user)

        # Redirect to login after successful registration
        return redirect('LoginPage')

    # If GET request → show register page
    return render(request, 'Register.html')


# Messages list + user search
@login_required
def MessagesView(request):
    my_profile = Profile.objects.get(user__username=request.user.username)
    my_chats = my_profile.chats.all()

    if request.method == "POST":
        query = request.POST.get('user')
        if query:
            # Search users by first or last name
            results = User.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            ).exclude(username=request.user.username)  # Exclude self
    else:
        results = []

    return render(request, 'Messages.html', {
        'results': results,
        'my_chats': my_chats
    })


# Individual chat page
@login_required
def ChatView(request, username):
    # Get names of chat participants
    speaking_partner_name = User.objects.get(
        username=username).first_name + " " + User.objects.get(username=username).last_name
    my_name = User.objects.get(username=request.user.username).first_name + \
        " " + User.objects.get(username=request.user.username).last_name

    my_profile = Profile.objects.get(user__username=request.user.username)

    # Check blocking status
    blocked = BlockedUsers.objects.filter(
        profile=my_profile, username=username).exists()
    his_profile = Profile.objects.get(user__username=username)
    youAreBlocked = BlockedUsers.objects.filter(
        profile=his_profile, username=request.user.username).exists()

    try:
        # Get or create chat with user
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
            # Add new message to my chat
            my_message = Message.objects.create(
                chat=ourChat,
                content=query,
                sender=request.user.username,
                receiver=username,
            )

            # Add mirrored message to partner's chat
            his_chat, _ = Chat.objects.get_or_create(
                profile=his_profile,
                speaking_partner=my_name,
                speaking_partner_username=request.user.username
            )
            his_message = Message.objects.create(
                chat=his_chat,
                content=query,
                sender=request.user.username,
                receiver=username,
                his_message_id=my_message.id
            )

            # Sync message IDs
            my_message.his_message_id = his_message.id
            my_message.save(update_fields=["his_message_id"])

    return render(request, 'Chat.html', {
        'speaking_partner_name': speaking_partner_name,
        'messages': messages,
        'blocked': blocked,
        'username': username,
        'youAreBlocked': youAreBlocked
    })


# Show delete message confirmation page
@login_required
def MessageDelete(request, message_id, username, his_message_id):
    my_message = Message.objects.get(id=message_id)
    his_message = Message.objects.get(id=his_message_id)

    chat = my_message.chat
    messages = chat.messages.all()
    speaking_partner_name = chat.speaking_partner

    return render(request, 'DeletePage.html', {
        'messages': messages,
        'speaking_partner_name': speaking_partner_name,
        'message': my_message,
        'his_message': his_message,
        'username': username
    })


# Confirm message deletion
@login_required
def Message_delete_confirm(request, message_id, username, his_message_id):
    # Delete both copies of the message
    Message.objects.get(id=message_id).delete()
    Message.objects.get(id=his_message_id).delete()
    return redirect('ChatPage', username=username)


# Show edit message page
@login_required
def MessageEdit(request, message_id, username, his_message_id):
    my_message = Message.objects.get(id=message_id)
    his_message = Message.objects.get(id=his_message_id)

    chat = my_message.chat
    messages = chat.messages.all()
    speaking_partner_name = chat.speaking_partner

    return render(request, 'EditPage.html', {
        'messages': messages,
        'speaking_partner_name': speaking_partner_name,
        'message': my_message,
        'his_message': his_message,
        'username': username
    })


# Confirm message editing
@login_required
def MessageEditConfirm(request, message_id, username, his_message_id):
    edited_value = request.POST.get('edited')

    # Update both messages with new content
    my_message = Message.objects.get(id=message_id)
    my_message.content = edited_value
    my_message.save(update_fields=["content"])

    his_message = Message.objects.get(id=his_message_id)
    his_message.content = edited_value
    his_message.save(update_fields=["content"])

    return redirect('ChatPage', username=username)


# Show delete chat confirmation page
@login_required
def DeleteChat(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    return render(request, 'DeleteChat.html', {'chat': chat})


# Confirm chat deletion
@login_required
def DeleteChatConfirm(request, chat_id):
    Chat.objects.get(id=chat_id).delete()
    return redirect('MessagesPage')


# Logout view
def logout_view(request):
    logout(request)
    return redirect("LoginPage")


# Block a user
@login_required
def BlockUser(request, username):
    my_profile = Profile.objects.get(user__username=request.user.username)
    BlockedUsers.objects.create(profile=my_profile, username=username)
    return redirect('ChatPage', username=username)


# Unblock a user
@login_required
def UnblockUser(request, username):
    my_profile = Profile.objects.get(user__username=request.user.username)
    BlockedUsers.objects.get(profile=my_profile, username=username).delete()
    return redirect('ChatPage', username=username)
