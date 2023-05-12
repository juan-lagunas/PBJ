from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import DarkMode

# Create your views here.

def index(request):
    if request.method == 'POST':
        try:
            mode = DarkMode.objects.get(dark=False)
            mode.dark=True
            mode.save()
            text = "text-white"
            background = "bg-zinc-900"
            navground = "bg-zinc-700"
            shadow = "drop-shadow-xl"
        except:
            mode = DarkMode.objects.get(dark=True)
            mode.dark=False
            mode.save()
            text = "text-black"
            background = "bg-gray-300"
            navground = "bg-gray-200"
            shadow = "drop-shadow-sm"


        return render(request, 'core/base.html', {
            'text': text,
            'background': background,
            'navground': navground
        })
    
    if request.method == 'GET':
        mode = DarkMode.objects.get(pk=1)
        if mode.dark == True:
            text = "text-white"
            background = "bg-zinc-900"
            navground = "bg-zinc-700"
            shadow = "drop-shadow-xl"
            return render(request, 'core/base.html', {
                'text': text,
                'background': background,
                'navground': navground,
                'shadow': shadow
            })
        else:
            return render(request, 'core/index.html')
        

def signup(request):
    return render(request, 'core/signup.html',)