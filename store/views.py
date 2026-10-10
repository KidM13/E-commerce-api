from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CategorySerializer,ProductSerializer,CartSerializer,CartItemSerializer,OrderSerializer,OrderItemSerializer
from .permission import IsAdminOrReadOnly,IsCartItemOwner,IsCartOwner,IsOrderOwnerOrStaffReadOnly
from .models import Category,Product,Cart,Cart_item,Order,Order_item
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

class CategoryViewset(viewsets.ModelViewSet):
    serializer_class=CategorySerializer
    permission_classes=[IsAdminOrReadOnly]
    queryset=Category.objects.all()
class ProductViewset(viewsets.ModelViewSet):
    serializer_class=ProductSerializer
    permission_classes=[IsAdminOrReadOnly]
    queryset=Product.objects.all()

def parse_int(value):
    """Convert to int, but reject booleans (True would otherwise become 1)."""
    if isinstance(value, bool):
        raise ValueError
    return int(value)
class CartViewset(viewsets.ModelViewSet):
    serializer_class=CartSerializer
    permission_classes=[IsCartOwner]
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_cart(self, request):
        # 1. The user's own cart, created the first time they need it
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # 2. Validate and fetch the product
        try:
            product_id = parse_int(request.data.get("product_id"))
        except (ValueError, TypeError):
            return Response(
                {"error": "product_id is required and must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 3. Validate quantity
        try:
            quantity = parse_int(request.data.get("quantity", 1))
        except (ValueError, TypeError):
            return Response(
                {"error": "Quantity must be a valid integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if quantity < 1:
            return Response(
                {"error": "Quantity must be at least 1."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 4. Is this product already in the cart?
        item = Cart_item.objects.filter(cart=cart, product=product).first()
        new_quantity = quantity + (item.quantity if item else 0)

        # 5. Courtesy stock check (checkout re-checks inside a transaction)
        if new_quantity > product.stock_count:
            return Response(
                {"error": "Not enough stock available."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 6. Update the existing row or create a new one
        if item:
            item.quantity = new_quantity
            item.save(update_fields=["quantity"])
            response_status = status.HTTP_200_OK
        else:
            item = Cart_item.objects.create(cart=cart, product=product, quantity=quantity)
            response_status = status.HTTP_201_CREATED

        # 7. Return the result
        return Response(
            {
                "message": "Item added to cart successfully.",
                "product": product.name,
                "quantity": item.quantity,
            },
            status=response_status,
        )