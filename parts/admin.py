from django.contrib import admin

from .models import Category, Part

# Register your models here.

class AdminCategory(admin.ModelAdmin):
    list_display = ('id', 'category')

class AdminPart(admin.ModelAdmin):
    list_display = ('id', 'partname', 'category', 'description', 'price', 'user', 'date')

    admin.site.register(Category, AdminCategory)
admin.site.register(Part, AdminPart)