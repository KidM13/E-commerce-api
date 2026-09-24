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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
class Cart_item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
class Order_item(models.Model):
    Order=models.ForeignKey(models.CASCADE)
    Product=models.ForeignKey(models.CASCADE)
    quantity=models.IntegerField()