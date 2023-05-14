from django.contrib import admin

from .models import Category, Part, Inventory, Logs
# Register your models here.
class AdminCategory(admin.ModelAdmin):
    list_display = ('id', 'category')

class AdminPart(admin.ModelAdmin):
    list_display = ('id', 'partname', 'category', 'descrition', 'price', 'user', 'date')

class AdminInventory(admin.ModelAdmin):
    list_display = ('id', 'partname', 'category', 'price', 'quantity',)
    
class AdminLogs(admin.ModelAdmin):
    list_display = ('id', 'partname', 'category', 'price', 'quantity', 'user', 'date')




admin.site.register(Category)
admin.site.register(Part)
admin.site.register(Inventory)
admin.site.register(Logs)
