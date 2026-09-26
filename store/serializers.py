from rest_framework import serializers
from .models import Category,Product,Cart,Cart_item,Order,Order_item

class CategorySerializer(serializers.Modelserializer):
    class Meta:
        model=Category
        fields=['name']
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['name','description','price','stock_count','category']