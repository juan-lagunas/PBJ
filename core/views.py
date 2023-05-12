from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import DarkMode

# Create your views here.
# mode = DarkMode.objects.get(dark=False)
# mode.dark=True
# mode.save()
# text = "text-white"
# background = "bg-zinc-900"
# navground = "bg-zinc-700"
# shadow = "drop-shadow-xl"

# mode = DarkMode.objects.get(dark=True)
# mode.dark=False
# mode.save()
# text = "text-black"
# background = "bg-gray-300"
# navground = "bg-gray-200"
# shadow = "drop-shadow-sm"
theme = {
    'body': 'bg-gray-300',
    'nav': 'bg-gray-200',
    'shadow': 'drop-shadow-sm',
}

def index(request):
    # If no user redirect to sign in page
    if not request.user.is_authenticated:
        return redirect('signin')
    
    # Else display user home page
    return render(request, 'core/index.html', {
        'theme': theme,
    })
    

def signin(request):
    if request.method == 'POST':
        username = request.POST['username'].title()
        password = request.POST['password']

        # Check that user filled out both username and password
        if not username or not password:
            return render(request, 'website/index.html', {
                'message': 'Please fill out both username and password.',
                'theme': theme,
            })
        
        # Check if user in database
        user = authenticate(request, userername=username, password=password)
        if user is None:
            return redirect(request, 'core/signin.html', {
                'message': 'Could not find username and password. Try again.',
                'theme': theme,
            })
        else:
            login(request, user)
            return redirect('index')

    return render(request, 'core/signin.html', {
        'theme': theme
    })


def signup(request):
    if request.method == 'POST':
        username = request.POST['username'].title()
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']

        # Check that user filled out form correctly and username available
        if not username or not email or not password or not confirmation:
            return render(request, 'core/signup.html', {
                'message': 'Please fill out all fields.',
                'theme': theme,
            })
        
        if password != confirmation:
            return render(request, 'core/signup.html', {
                'message': 'Passwords do not match.'
            })
        
        if User.objects.filter(username=username).exists():
            return render(request, 'core/signup.html', {
                'message': 'Username already taken.',
                'theme': theme,
            })
        
        # Create user
        user = User.objects.creat_user(username, email, password)
        user.save()
        return render(request, 'core/signin.html', {
            'message': 'Successfull singed up.',
            'theme': theme,
        })

    return render(request, 'core/signup.html', {
        'theme': theme
    })


def apology(request, apology):
    return render(request,)

def theme(request):
    pass

