from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.

def Login(request):
     if request.method == "POST":
          username = request.POST.get('Username')
          password = request.POST.get('Password')

          user = authenticate(request, username=username, password=password)

          if user is not None:
               login(request, user)
               return redirect('ProfilePage')
          else:
               error = "False login or password" 
               return render (request, 'Login.html', {'error' : error})

     return render (request, 'Login.html')

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
        User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
        return redirect('LoginPage')  # После регистрации — на логин

    return render(request, 'Register.html')
     

def Profile(request):
     if request.method == "POST":
        query = request.POST.get('user')
        if query:
            results = User.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
     else:
         results = []
     return render(request, 'Profile.html', {'results' : results})