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
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart_item
        fields=['id','cart','product','quantity']
        read_only_fields = ['cart']
    def validate(self, attrs):
        product = attrs.get(
            'product',
            self.instance.product if self.instance else None
        )
        quantity = attrs.get(
            'quantity',
            self.instance.quantity if self.instance else None
        )

        if quantity is not None and quantity <= 0:
            raise serializers.ValidationError({
                'quantity': 'Quantity must be greater than zero.'
            })

        if product and quantity is not None:
            if quantity > product.stock_count:
                raise serializers.ValidationError({
                    'quantity': (
                        f'Only {product.stock_count} units '
                        'are available in stock.'
                    )
                })

     return attrs

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['id','user','status','created_at']
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order_item
        fields=['id','order','product','quantity','price_at_purchase']
        read_only_fields=['price_at_purchase']





