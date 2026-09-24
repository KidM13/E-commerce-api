from django.db import models

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=250)
    description=models.TextField()
    price=models.DecimalField()
    stock_count=models.IntegerField()
class Category(models.Model):
    name=models.CharField()
    Product=models.ForeignKey(models.CASCADE)
class Cart(models.Model):
    
class Cart_item(models.Model):
    Product=models.ForeignKey(models.CASCADE)
    quantity=models.IntegerField()
    Cart=models.ForeignKey(models.CASCADE)
class Order(models.Model):
    status=models.CharField()
class Order_item(models.Model):
    Order=models.ForeignKey(models.CASCADE)
    Product=models.ForeignKey(models.CASCADE)
    quantity=models.IntegerField()