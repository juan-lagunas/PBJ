from django.contrib import admin

from .models import Category, Part, Inventory, Log

class AdminCategory(admin.ModelAdmin):
    list_display = ('id', 'category')

class AdminPart(admin.ModelAdmin):
    list_display = ('id', 'partname', 'category', 'description', 'price', 'user', 'date')

class AdminInventory(admin.ModelAdmin):
    list_display = ('id', 'partname', 'category', 'quantity', 'usd', 'total')
    
class AdminLog(admin.ModelAdmin):
    list_display = ('id', 'partname', 'category', 'quantity', 'total', 'user', 'date')


admin.site.register(Category, AdminCategory)
admin.site.register(Part, AdminPart)
admin.site.register(Inventory, AdminInventory)
admin.site.register(Log, AdminLog)
