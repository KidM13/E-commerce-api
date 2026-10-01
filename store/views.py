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