from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter
router.register('api/Category-v2',views.CategoryViewset)
router.register('api/product-v2',views.ProductViewset)
router.register('api/cart-v2',views.CartViewset)
router.register('api/order-v2',views.OrderViewset)
url_patterns=[]+router.urls