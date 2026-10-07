from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('api/category',views.CategoryViewset)
router.register('api/product',views.ProductViewset)
router.register('api/cart',views.CartViewset)
router.register('api/cart-items', views.CartItemViewset)
router.register('api/order',views.OrderViewset)
router.register('api/order-items', views.OrderItemViewset)
urlpatterns=[]+router.urls