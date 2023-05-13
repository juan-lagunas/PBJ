from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import DarkMode
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import datetime


@login_required
def index(request):
    today = datetime.date.today()
    # If user has a theme load theme else create default theme
    try:
        theme = DarkMode.objects.get(user=request.user.username)
        return render(request, 'core/index.html', {
            'theme': theme,
            'date': today
        })
    except:
        theme = DarkMode.objects.create(user = request.user.username)
        return render(request, 'core/index.html', {
            'theme': theme,
            'date': today
        })
    # Else display user home page
    
    

def signin(request):
    theme = {
        'body': 'bg-slate-300 text-slate-800',
        'nav': 'drop-shadow-md bg-slate-200',
        'hover': 'hover:bg-slate-700 hover:text-slate-200',
    }
    if request.method == 'POST':
        username = request.POST['username'].title()
        password = request.POST['password']

        # Check that user filled out both username and password
        if not username or not password:
            return render(request, 'core/login.html', {
                'message': 'Please fill out both Username and Password.',
                'theme': theme,
            })
        
        # Check if user in database
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'core/login.html', {
                'message': 'Could not find Username and Password. Try again.',
                'theme': theme
            })

    return render(request, 'core/login.html', {
        'theme': theme
    })


def signup(request):
    theme = {
        'body': 'bg-slate-300 text-slate-800',
        'nav': 'drop-shadow-md bg-slate-200',
        'hover': 'hover:bg-slate-700 hover:text-slate-200',
    }
    if request.method == 'POST':
        username = request.POST['username'].title()
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']

        # Check that user filled out form correctly and username available
        if not username or not email or not password or not confirmation:
            return render(request, 'core/signup.html', {
                'message': 'Please fill out all fields.',
                'theme': theme
            })
        
        if password != confirmation:
            return render(request, 'core/signup.html', {
                'message': 'Passwords do not match.',
                'theme': theme
            })
        
        if User.objects.filter(username=username).exists():
            return render(request, 'core/signup.html', {
                'message': 'Username already taken.',
                'theme': theme
            })
        
        # Create user
        user = User.objects.create_user(username, email, password)
        user.save()
        return render(request, 'core/login.html', {
            'message': 'Successfully signed up.',
            'theme': theme
        })

    return render(request, 'core/signup.html', {
        'theme': theme
    })


def signout(request):
    theme = {
        'body': 'bg-slate-300 text-slate-800',
        'nav': 'drop-shadow-md bg-slate-200',
        'hover': 'hover:bg-slate-700 hover:text-slate-200',
    }

    logout(request)
    return redirect('/')


def theme(request):
    # Get the mode user has selected and change colors accordingly
    mode = request.GET.get('mode')

    if mode == 'Dark':
        theme = DarkMode.objects.get(user=request.user.username)
        if theme.mode == 'Dark':
            return redirect('/')
        
        theme.mode = 'Dark'
        theme.body = 'bg-zinc-900 text-white'
        theme.nav = 'drop-shadow-xl bg-zinc-800'
        theme.hover = 'hover:bg-gray-200 hover:text-gray-900'
        theme.save()
    elif mode == 'Light':
        theme = DarkMode.objects.get(user=request.user.username)
        if theme.mode == 'Light':
            return redirect('/')
        
        theme.mode = 'Light'
        theme.body = 'bg-slate-300 text-slate-800'
        theme.nav = 'drop-shadow-sm bg-slate-200'
        theme.hover = 'hover:bg-slate-700 hover:text-slate-200'
        theme.save()

    return redirect('/')