from rest_framework import serializers
from .models import Category,Product,Cart,Cart_item,Order,Order_item

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name']
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','description','price','stock_count','category']
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=['id','user']
        read_only_fields=['user']
class Cart_itemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart_item
        fields=['id','cart','product','quantity']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['id','user','status','created_at']
class Order_itemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order_item
        fields=['id''order','product','quantity','price_at_purchase']




