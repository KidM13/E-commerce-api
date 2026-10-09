from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CategorySerializer,ProductSerializer,CartSerializer,CartItemSerializer,OrderSerializer,OrderItemSerializer
from .permission import IsAdminOrReadOnly,IsCartItemOwner,IsCartOwner,IsOrderOwnerOrStaffReadOnly
from .models import Category,Product,Cart,Cart_item,Order,Order_item
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

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
    def add_to_cart(self, request, pk=None):
        # 1. Get the cart belonging to the current user
        cart = self.get_object()

        # 2. Get the product and requested quantity
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        product = get_object_or_404(Product, id=product_id)

        # 3. Validate quantity
        try:
            if isinstance(quantity, bool):
                raise ValueError
            quantity = int(quantity)
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

        # 4. Check whether this product is already in the cart
        item = Cart_item.objects.filter(
            cart=cart,
            product=product,
        ).first()

        new_quantity = quantity
        if item:
            new_quantity += item.quantity

        # 5. Check stock before changing the database
        if new_quantity > product.stock_count:
            return Response(
                {"error": "Not enough stock available."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 6. Create the item or update its quantity
        if item:
            item.quantity = new_quantity
            item.save(update_fields=["quantity"])
        else:
            item = Cart_item.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
            )

        # 7. Return the result
        return Response(
            {
                "message": "Item added to cart successfully.",
                "product": product.name,
                "quantity": item.quantity,
            },
            status=status.HTTP_200_OK,
        )