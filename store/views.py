from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CategorySerializer
from .permission import IsAdminOrReadOnly
from .models import Category

class CategoryViewset(viewsets.ModelViewSet):
    serializer_class=CategorySerializer
    permission_classes=[IsAdminOrReadOnly]
    queryset=Category.objects.all()