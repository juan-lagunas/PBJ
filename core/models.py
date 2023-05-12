from django.db import models

# Create your models here.
class DarkMode(models.Model):
    dark = models.BooleanField(default=False)

    def __self__(self):
        return self.id
