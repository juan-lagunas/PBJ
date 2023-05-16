from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import DarkMode
from django.contrib.auth.decorators import login_required
import datetime
from .models import Inventory, Log
from parts.models import Part, Category
from core.models import DarkMode
from django.db.models import Sum
import math

# Inventory home
@login_required
def index(request):
    theme = DarkMode.objects.filter(user=request.user.username)[0]
    inventory = Inventory.objects.all()[:20]
    total = 0
    for part in inventory:
        total += part.price * part.quantity

    return render(request, 'inventory/index.html', {
        'theme': theme,
        'inventory': inventory,
        'total': f'${total:,.2f}' 
    })


# Display inventory
@login_required
def stock(request):
    theme = DarkMode.objects.filter(user=request.user.username)[0]
    inventory = Inventory.objects.all().order_by('-quantity')[:10]
    part_count = Inventory.objects.aggregate(Sum('quantity'))
    total = 0
    for part in inventory:
        total += part.price * part.quantity

    # Handles search
    if request.method == 'POST' and 'search' in request.POST:
        part = request.POST['part_name'].title()
        if not part:
            return render(request, 'inventory/stock.html', {
                'theme': theme,
                'inventory': inventory,
                'part_count': part_count,
                'total': f'${total:,.2f}',
                'fail': 'Could not find part.'
            })

        try:
            part_data = Inventory.objects.filter(partname__contains=part)
        except:
            return render(request, 'inventory/stock.html', {
                'theme': theme,
                'inventory': inventory,
                'part_count': part_count,
                'total': f'${total:,.2f}',
                'fail': 'Could not find part.'
            })

        return render(request, 'inventory/stock.html', {
            'theme': theme,
            'inventory': part_data,
            'part_count': part_count,
            'total': f'${total:,.2f}',
            'success': 'success'
        })
    
    return render(request, 'inventory/stock.html', {
        'theme': theme,
        'inventory': inventory,
        'part_count': part_count,
        'total': f'${total:,.2f}'
    })

@login_required
def page(request):
    theme = DarkMode.objects.filter(user=request.user.username)[0]
    parts = Inventory.objects.count()
    pages = math.ceil(parts/10)
    inventory = Inventory.objects.all()[:10]
    if request.method == 'GET':
        return render(request, 'inventory/page.html', {
            'theme': theme,
            'pages': range(1,pages+1),
            'inventory': inventory
        })
    
    if request.method == 'POST':
        try:
            page = int(request.POST['page'])
        except ValueError:
            return render(request, 'inventory/page.html', {
                'fail': 'Page not founds',
                'theme': theme,
                'inventory': inventory,
                'pages': range(1,pages+1),
            })

        if page > pages or page < 0:
            return render(request, 'inventory/page.html', {
                'fail': 'Page not found',
                'theme': theme,
                'inventory': inventory,
                'pages': range(1,pages+1),
            })
        
        inventory = Inventory.objects.all()[page*10-10:page*10]
        return render(request, 'inventory/page.html', {
            'theme': theme,
            'pages': range(1,pages+1),
            'inventory': inventory
        })

            


# Add inventory
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
    

# Show logs
@login_required
def logs(request):
    logs = Log.objects.all().order_by('-date')[:15]
    theme = DarkMode.objects.filter(user=request.user.username)[0]
    return render(request, 'inventory/logs.html', {
        'theme': theme,
        'logs': logs,
})


# Checkout parts
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
        
    
# Edit inventory    
@login_required
def edit(request):
    theme = DarkMode.objects.filter(user=request.user.username)[0]
    # Handles search
    if request.method == 'POST' and 'search' in request.POST:      
        part_name = request.POST['part_name'].title()
        if not part_name:
            return render(request, 'inventory/edit.html', {
                'theme': theme,
                'search': 'Could not find part.'
            })
    
        part_inventory = Inventory.objects.filter(partname__contains=part_name)
        if not part_inventory:
            return render(request, 'inventory/edit.html', {
                'theme': theme,
                'search': 'Part not found.'
            })

        return render(request, 'inventory/edit.html', {
                'theme': theme,
                'parts': part_inventory
            })

    # Handles changing info   
    if request.method == 'POST' and 'edit' in request.POST:
        try:
            part = request.POST['part'].title()
            name = request.POST['name'].title()
            category = request.POST['category'].title()
            price = float(request.POST['price'])
            if not part or not name or not category or not price:
                return render(request, 'inventory/edit.html', {
                    'theme': theme,
                    'fail': 'Need to fill out everything.'
                })
        except ValueError:
            return render(request, 'inventory/edit.html', {
                'theme': theme,
                'fail': 'Failed to input valid price.'
            })
        
        try:
            part_data = Part.objects.get(partname=part)
        
        except:
            return render(request, 'inventory/edit.html', {
                'theme': theme,
                'fail': 'Part not found.'
            })
        
    else:
        return render(request, 'inventory/edit.html', {
            'theme': theme
        })