from django.contrib import admin
from .models import DarkMode

# Register your models here.
class DarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'mode', 'body', 'nav', 'shadow')

admin.site.register(DarkMode, DarkAdmin)

