from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import DarkMode
from django.contrib.auth.decorators import login_required
import datetime
from .models import Part, Category
from core.models import DarkMode

# Create your views here.

@login_required
def index(request):
    theme = DarkMode.objects.filter(user=request.user.username)[0]
    return render(request, 'parts/index.html', {
        'theme': theme
    })

# Create new part
@login_required
def add(request):
    theme = DarkMode.objects.filter(user=request.user.username)[0]
    if request.method == 'POST':
        try:
            price = float(request.POST['price'])
        except ValueError:
            return render(request, 'parts/add.html', {
                'fail': 'Need to fill out everything.',
                'theme': theme
            })
        
        part = request.POST['part'].title()
        category = request.POST['category'].title()
        description = request.POST['description'].capitalize()
        user_submitting = request.user.username
        date = datetime.date.today()

        if not part or not category or not price or not description or not user_submitting or not date:
            return render(request, 'parts/add.html', {
                'fail': 'Need to fill out everything.',
                'theme': theme
            })
        
        category_data = Category.objects.filter(category=category)
        partdata = Part.objects.filter(partname=part)
        if category_data.exists():
            if Part.objects.filter(partname=part).exists():
                return render(request, 'parts/add.html', {
                    'fail': 'Part already exists',
                    'theme': theme
                })
            else:
                Part.objects.create(
                    partname = part,
                    category = category_data.first(),
                    description = description,
                    price = price,
                    user = user_submitting,
                    date = date,
                )
        else:      
            if partdata.exists():
                return render(request, 'parts/add.html', {
                    'fail': 'Category has been created, but part already exists..',
                    'theme': theme
                })
            else:
                Category.objects.create(category=category)
                Part.objects.create(
                    partname = part,
                    category = Category.objects.get(category=category),
                    description = description,
                    price = price,
                    user = user_submitting,
                    date = date,
                )

        return render(request, 'parts/add.html', {
            'success': 'Part information saved!',
            'theme': theme
        })
    
    else: 
        return render(request, 'parts/add.html', {
            'theme': theme
        })


# Edit parts    
@login_required
def edit(request):
    theme = DarkMode.objects.filter(user=request.user.username)[0]
    if request.method == 'POST' and 'search' in request.POST:      
        part_name = request.POST['part_name'].title()
        if not part_name:
            return render(request, 'parts/edit.html', {
                'theme': theme,
                'search': 'Could not find part.'
            })
        
    
        parts = Part.objects.filter(partname__contains=part_name)
        if not parts:
            return render(request, 'parts/edit.html', {
                'theme': theme,
                'search': 'Part not found.'
            })

        return render(request, 'parts/edit.html', {
                'theme': theme,
                'parts': parts
            })
        
    if request.method == 'POST' and 'edit' in request.POST:
        part = request.POST['part'].title()
        name = request.POST['name'].title()
        category = request.POST['category'].title()
        if not part or not name or not category:
            return render(request, 'parts/edit.html', {
                'theme': theme,
                'fail': 'Need to fill out everything.'
            })
        
        try:
            price = float(request.POST['price'])
        except ValueError:
            return render(request, 'parts/edit.html', {
                'theme': theme,
                'fail': 'Failed to input valid price.'
            })
        
        try:
            part_data = Part.objects.get(partname=part)
        except:
            return render(request, 'parts/edit.html', {
                'theme': theme,
                'fail': 'Part not found.'
            })
        
        message = ''
        try:
            category_data = Category.objects.get(category=category)
        except:
            category_data = Category.objects.create(category=category)
            message += 'New category was created. '
        
        part_data.partname = name
        part_data.category = category_data
        part_data.price = price
        part_data.save()

        return render(request, 'parts/edit.html', {
            'theme': theme,
            'success': message + 'Part updated.'
        })
   
    else:
        return render(request, 'parts/edit.html', {
            'theme': theme
        })