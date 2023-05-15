from django.db import models

class Category(models.Model):
    category = models.CharField(max_length=64)
    
    def __str__(self):
        return f'{self.category}'
    

class Part(models.Model):
    partname = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    user = models.CharField(max_length=40)
    date = models.DateField()

    @property
    def usd(self):
        return f'${self.price:,.2f}'

    def __str__(self):
        return f'{self.partname} ({self.category}) - {self.description} : ${self.usd}'
    