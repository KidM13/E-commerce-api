from django.contrib import admin

from .models import Category,Product,Cart,Cart_item,Order_item,Order
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Cart_item)
admin.site.register(Order)
admin.site.register(Order_item)

