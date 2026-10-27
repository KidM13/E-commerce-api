from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('api/category',views.CategoryViewset)
router.register('api/product',views.ProductViewset)
router.register('api/cart',views.CartViewset,basename='cart')
router.register('api/cart-items', views.CartItemViewset,basename='cart_item')
router.register('api/order',views.OrderViewset,basename='order')
router.register('api/order-items', views.OrderItemViewset,basename='order_item')
urlpatterns=[]+router.urls
