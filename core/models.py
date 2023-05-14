from django.db import models

# Create your models here.
class DarkMode(models.Model):
    user = models.CharField(max_length=64)
    mode = models.CharField(max_length=64, default='Light')
    body = models.CharField(max_length=64, default='bg-slate-300 text-slate-800')
    nav = models.CharField(max_length=64, default='drop-shadow-sm bg-slate-200')
    hover = models.CharField(max_length=64, default='hover:bg-slate-700 hover:text-slate-200')

    def __self__(self):
        return self.mode
