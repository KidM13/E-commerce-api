from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=250)
    def __str__(self):
        return self.name
class Product(models.Model):
    name=models.CharField(max_length=250)
    description=models.TextField()
    price=models.DecimalField()
    stock_count=models.IntegerField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Cart(models.Model):
    
class Cart_item(models.Model):
    Product=models.ForeignKey(models.CASCADE)
    quantity=models.IntegerField()
    Cart=models.ForeignKey(models.CASCADE)
class Order(models.Model):
    status=models.CharField(max_length=250)
class Order_item(models.Model):
    Order=models.ForeignKey(models.CASCADE)
    Product=models.ForeignKey(models.CASCADE)
    quantity=models.IntegerField()