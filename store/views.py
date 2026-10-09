from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CategorySerializer,ProductSerializer,CartSerializer,CartItemSerializer,OrderSerializer,OrderItemSerializer
from .permission import IsAdminOrReadOnly,IsCartItemOwner,IsCartOwner,IsOrderOwnerOrStaffReadOnly
from .models import Category,Product,Cart,Cart_item,Order,Order_item
from rest_framework.decorators import action
from rest_framework.response import Response

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
    @action(detail=True,methods=['POST'])
    def add_to_cart(request):
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)

    product = get_object_or_404(Product, id=product_id)

    # Validate quantity
    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return Response(
            {"error": "Quantity must be an integer."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if quantity < 1:
        return Response(
            {"error": "Quantity must be at least 1."},
            status=status.HTTP_400_BAD_REQUEST
        )

    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": quantity}
    )

    if not created:
        item.quantity += quantity

    if item.quantity > product.stock:
        return Response(
            {"error": "Not enough stock available."},
            status=status.HTTP_400_BAD_REQUEST
        )

    item.save()

    return Response(
        {
            "message": "Item added to cart successfully.",
            "product": product.name,
            "quantity": item.quantity
        },
        status=status.HTTP_200_OK
    )

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