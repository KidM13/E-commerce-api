from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CategorySerializer,ProductSerializer,CartSerializer,CartItemSerializer,OrderSerializer,OrderItemSerializer
from .permission import IsAdminOrReadOnly,IsCartItemOwner,IsCartOwner,IsOrderOwnerOrStaffReadOnly
from .models import Category,Product,Cart,Cart_item,Order,Order_item

class CategoryViewset(viewsets.ModelViewSet):
    serializer_class=CategorySerializer
    permission_classes=[IsAdminOrReadOnly]
    queryset=Category.objects.all()
class ProductViewset(viewsets.ModelViewSet):
    serializer_class=ProductSerializer
    permission_classes=[IsAdminOrReadOnly]
    queryset=Product.objects.all()
class CartViewset(viewsets.ModelViewSet):
    serializer_class=CartSerializer
    permission_classes=[IsCartOwner]
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
class CartItemViewset(viewsets.ModelViewSet):
    serializer_class=CartItemSerializer
    permission_classes=[IsCartItemOwner]
    queryset=Cart_item.objects.select_related('cart')
class OrderViewset(viewsets.ModelViewSet):
    serializer_class=OrderSerializer
    permission_classes=[IsOrderOwnerOrStaffReadOnly]
    def get_queryset(self):
       user=self.request.user
       if user.is_staff:
           return Order.objects.all()
       return Order.objects.filter(user=user)
    
class OrderItemViewset(viewsets.ModelViewSet):
    serializer_class=OrderItemSerializer
    queryset=Order_item.objects.select_related('order')