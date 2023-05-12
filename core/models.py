from django.db import models

# Create your models here.
class DarkMode(models.Model):
    user = models.CharField(max_length=64)
    mode = models.CharField(max_length=64, default="Light")
    body = models.CharField(max_length=64, default="bg-gray-300 text-slate-700")
    nav = models.CharField(max_length=64, default="bg-gray-200 drop-shadow-sm")

    def __self__(self):
        return self.mode
