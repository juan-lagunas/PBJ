from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import DarkMode
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    theme = DarkMode.objects.get(user=request.user.username)
    return render(request, 'inventory/index.html', {
        'theme': theme 
    })


@login_required
def add(request):
    if request.method == 'POST':
        pass

    theme = DarkMode.objects.get(user=request.user.username)
    return render(request, 'inventory/add.html', {
        'theme': theme
    })
