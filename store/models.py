from django.db import models

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=250)
    description=models.TextField()
    price=models.IntegerField()
    stock_count=models.IntegerField()
class Category(models.Model):
    name=models.CharField()
    Product=models.ForeignKey(models.CASCADE)