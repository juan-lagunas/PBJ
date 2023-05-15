from django.contrib import admin

from .models import Inventory, Log

class AdminInventory(admin.ModelAdmin):
    list_display = ('id', 'partname', 'category', 'quantity', 'usd', 'total')
    
class AdminLog(admin.ModelAdmin):
    list_display = ('id', 'partname', 'category', 'quantity', 'total', 'user', 'date')

admin.site.register(Inventory, AdminInventory)
admin.site.register(Log, AdminLog)
