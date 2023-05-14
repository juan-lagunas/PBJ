from django.db import models

# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=64)
    
    def __self__(self):
        return f'{self.id}: {self.category}'
    
class Part(models.Model):
    partname = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    user = models.CharField(max_length=40)
    date = models.DateField()

    def __self__(self):
        return f'{self.partname} ({self.category}) - {self.description} : ${self.price}'
    
class Inventory(models.Model):
    partname = models.CharField(max_length=100)
    category = models.CharField(max_length=64)
    price = models.FloatField()
    quantity = models.IntegerField()

    @property
    def total(self):
        value = self.price * self.quantity
        return f'{value:,.2f}'
    
    @property
    def usd(self):
        return f'{self.price:,.2f}'

    def __self__(self):
        return f'{self.partname} ({self.category}) - Qty: {self.quantity} Price: ${self.price} Total: %{self.total}'
    
class Logs(models.Model):
    partname = models.CharField(max_length=100)
    category = models.CharField(max_length=64)
    price = models.FloatField()
    quantity = models.IntegerField()
    user = models.CharField(max_length=40)
    date = models.DateTimeField()

    @property
    def usd(self):
        value = self.price * self.quantity
        return f'{value:,.2f}'
    
    def __self__(self):
        return f'{self.partname} ({self.category}) - Qty: {self.quantity} Price: ${self.price} User: {self.user} Date: {self.date}'