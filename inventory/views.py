from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import DarkMode
from django.contrib.auth.decorators import login_required
import datetime
from .models import Category, Part, Inventory, Log


# Inventory home
@login_required
def index(request):
    inventory = Inventory.objects.all()[:20]
    theme = DarkMode.objects.filter(user=request.user.username)[0]
    total = 0
    for part in inventory:
        total += part.price * part.quantity
    
    return render(request, 'inventory/index.html', {
        'theme': theme,
        'inventory': inventory,
        'total': f'${total:,.2f}' 
    })


# Create new part
@login_required
def new(request):
    theme = DarkMode.objects.filter(user=request.user.username)[0]
    if request.method == 'POST':
        try:
            price = float(request.POST['price'])
        except ValueError:
            return render(request, 'inventory/create.html', {
                'fail': 'Need to fill out everything.',
                'theme': theme
            })
        
        part = request.POST['part'].title()
        category = request.POST['category'].title()
        description = request.POST['description'].capitalize()
        user_submitting = request.user.username
        date = datetime.date.today()

        if not part or not category or not price or not description or not user_submitting or not date:
            return render(request, 'inventory/create.html', {
                'fail': 'Need to fill out everything.',
                'theme': theme
            })
        
        category_data = Category.objects.filter(category=category)
        partdata = Part.objects.filter(partname=part)
        if category_data.exists():
            if Part.objects.filter(partname=part).exists():
                return render(request, 'inventory/create.html', {
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
                return render(request, 'inventory/create.html', {
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

        return render(request, 'inventory/create.html', {
            'success': 'Part information saved!',
            'theme': theme
        })
    
    else: 
        return render(request, 'inventory/create.html', {
            'theme': theme
        })


# Add quantity to existing part
@login_required
def add(request):
    theme = DarkMode.objects.filter(user=request.user.username)[0]
    if request.method == 'POST':
        try:
            quantity = int(request.POST['quantity'])
        except ValueError:
            return render(request, 'inventory/add.html', {
                'theme': theme,
                'fail': 'Quantity has to be a whole number.'
            })
        part = request.POST['part'].title()

        if not part or not quantity:
            return render(request, 'inventory/add.html', {
                'theme': theme,
                'fail': 'Need to fill out both parts.'
            })
        
        try:
            partdata = Part.objects.get(partname=part)
        except:
            return render(request, 'inventory/add.html', {
                'theme': theme,
                'fail': 'Part not found.'
            })
        
        # If part in inventory update quantity else create
        if Inventory.objects.filter(partname=part).exists():
            inventory = Inventory.objects.get(partname=part)
            inventory.quantity += quantity
            inventory.save()
        else:
            Inventory.objects.create(
                partname = part,
                category = partdata.category,
                quantity = quantity,
                price = partdata.price
            )
        
        # Create a log entry
        date = datetime.datetime.now()
        user = request.user.username
        Log.objects.create(
            partname = partdata.partname,
            category = partdata.category,
            price = partdata.price,
            quantity = quantity,
            user = user,
            date = date,
        )

        return render(request, 'inventory/add.html', {
            'success': 'Updated inventory!',
            'theme': theme
        })
        
    else:
        return render(request, 'inventory/add.html', {
            'theme': theme
        })


@login_required
def logs(request):
    logs = Log.objects.all().order_by('-date')[:15]
    theme = DarkMode.objects.filter(user=request.user.username)[0]
    return render(request, 'inventory/logs.html', {
        'theme': theme,
        'logs': logs,
})

@login_required
def checkout(request):
    theme = DarkMode.objects.filter(user=request.user.username)[0]
    if request.method == 'POST':
        part = request.POST['part'].title()
        try:
            quantity = int(request.POST['quantity'])
        except ValueError:
            return render(request, 'inventory/checkout.html', {
                'theme': theme,
                'fail': 'Quantity has to be whole number.'
            })
        
        if not part or not quantity:
            return render(request, 'inventory/checkout.html', {
                'theme': theme,
                'fail': 'Need to fill out both parts.'
            })
        
        try:
            data = Inventory.objects.get(partname=part)
        except:
            return render(request, 'inventory/checkout.html', {
                'theme': theme,
                'fail': 'Part not found'
            })
        
        if quantity > data.quantity:
            return render(request, 'inventory/checkout.html', {
                'theme': theme,
                'fail': 'Not enough in stock.'
            })
        
        data.quantity -= quantity
        data.save()
        date = datetime.datetime.now()
        user = request.user.username

        Log.objects.create(
            partname = data.partname,
            category = data.category,
            price = data.price,
            quantity = -quantity,
            user = user,
            date = date,
        )

        return render(request, 'inventory/checkout.html', {
            'theme': theme,
            'success': 'Checkout complete.'
        })
    
    else:
        return render(request, 'inventory/checkout.html', {
            'theme': theme,
        })
        

@login_required
def editpart(request):
    theme = DarkMode.objects.filter(user=request.user.username)[0]
    if request.method == 'POST' and 'search' in request.POST:      
        part_name = request.POST['part_name'].title()
        if not part_name:
            return render(request, 'inventory/editpart.html', {
                'theme': theme,
                'search': 'Could not find part.'
            })
        
    
        parts = Part.objects.filter(partname__contains=part_name)
        if not parts:
            return render(request, 'inventory/editpart.html', {
                'theme': theme,
                'search': 'Part not found.'
            })

        return render(request, 'inventory/editpart.html', {
                'theme': theme,
                'parts': parts
            })
        
    if request.method == 'POST' and 'edit' in request.POST:
        try:
            part = request.POST['part'].title()
            name = request.POST['name'].title()
            category = request.POST['category'].title()
            price = float(request.POST['price'])
            if not part or not name or not category or not price:
                return render(request, 'inventory/editpart.html', {
                    'theme': theme,
                    'fail': 'Need to fill out everything.'
                })
        except ValueError:
            return render(request, 'inventory/editpart.html', {
                'theme': theme,
                'fail': 'Failed to input valid price.'
            })
        
        try:
            part_data = Part.objects.get(partname=part)
        
        except:
            return render(request, 'inventory/editpart.html', {
                'theme': theme,
                'fail': 'Part not found.'
            })
            

   
    else:
        return render(request, 'inventory/editpart.html', {
            'theme': theme
        })
    
@login_required
def editinventory(request):
    theme = DarkMode.objects.filter(user=request.user.username)[0]
    if request.method == 'POST' and 'search' in request.POST:      
        part_name = request.POST['part_name'].title()
        if not part_name:
            return render(request, 'inventory/editpart.html', {
                'theme': theme,
                'search': 'Could not find part.'
            })
        
    
        parts = Part.objects.filter(partname__contains=part_name)
        if not parts:
            return render(request, 'inventory/editpart.html', {
                'theme': theme,
                'search': 'Part not found.'
            })

        return render(request, 'inventory/editpart.html', {
                'theme': theme,
                'parts': parts
            })
        
    if request.method == 'POST' and 'edit' in request.POST:
        try:
            part = request.POST['part'].title()
            name = request.POST['name'].title()
            category = request.POST['category'].title()
            price = float(request.POST['price'])
            if not part or not name or not category or not price:
                return render(request, 'inventory/editpart.html', {
                    'theme': theme,
                    'fail': 'Need to fill out everything.'
                })
        except ValueError:
            return render(request, 'inventory/editpart.html', {
                'theme': theme,
                'fail': 'Failed to input valid price.'
            })
        
        try:
            part_data = Part.objects.get(partname=part)
        
        except:
            return render(request, 'inventory/editpart.html', {
                'theme': theme,
                'fail': 'Part not found.'
            })
            

   
    else:
        return render(request, 'inventory/editpart.html', {
            'theme': theme
        })