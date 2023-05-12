from django.db import models

# Create your models here.
class DarkMode(models.Model):
    user = models.CharField(max_length=20)
    mode = models.CharField(max_length=6, default="Light"),
    body = models.CharField(max_length=20, default="bg-gray-300"),
    nav = models.CharField(max_length=20, default="bg-gray-200"),
    shadow = models.CharField(max_length=15, default="drop-shadow-sm")

    def __self__(self):
        return self.mode
