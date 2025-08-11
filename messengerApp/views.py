from django.shortcuts import render

# Create your views here.

def Login(request):
     return render (request, 'Login.html')

def Register(request):
     return render (request, 'Register.html')