from django.test import TestCase

# Create your tests here.

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import (
    Category, Product, Cart, Cart_item, Order, Order_item
)

User = get_user_model()


class EcommerceAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='customer',
            password='testpass123'
        )

        self.admin = User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True
        )

        self.category = Category.objects.create(name='Electronics')

        self.product = Product.objects.create(
            name='Laptop',
            description='Test laptop',
            price=Decimal('1000.00'),
            stock_count=10,
            category=self.category
        )

    def test_products_are_publicly_accessible(self):
        response = self.client.get('/api/product/')

        self.assertEqual(response.status_code, 200)

    def test_customer_cannot_create_product(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/product/', {
            'name': 'Phone',
            'description': 'Test phone',
            'price': '500.00',
            'stock_count': 5,
            'category': self.category.id
        })

        self.assertEqual(response.status_code, 403)

    def test_admin_can_create_product(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post('/api/product/', {
            'name': 'Phone',
            'description': 'Test phone',
            'price': '500.00',
            'stock_count': 5,
            'category': self.category.id
        })

        self.assertEqual(response.status_code, 201)

    def test_add_to_cart(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/cart/add_to_cart/', {
            'product_id': self.product.id,
            'quantity': 2
        })

        self.assertEqual(response.status_code, 201)

        cart = Cart.objects.get(user=self.user)

        item = Cart_item.objects.get(
            cart=cart,
            product=self.product
        )

        self.assertEqual(item.quantity, 2)

    def test_adding_same_product_increases_quantity(self):
        self.client.force_authenticate(user=self.user)

        url = '/api/cart/add_to_cart/'

        self.client.post(url, {
            'product_id': self.product.id,
            'quantity': 2
        })

        response = self.client.post(url, {
            'product_id': self.product.id,
            'quantity': 3
        })

        self.assertEqual(response.status_code, 200)

        item = Cart_item.objects.get(
            cart__user=self.user,
            product=self.product
        )

        self.assertEqual(item.quantity, 5)

    def test_add_to_cart_rejects_insufficient_stock(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/cart/add_to_cart/', {
            'product_id': self.product.id,
            'quantity': 11
        })

        self.assertEqual(response.status_code, 400)

    def test_checkout(self):
        cart = Cart.objects.create(user=self.user)

        Cart_item.objects.create(
            cart=cart,
            product=self.product,
            quantity=3
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/order/checkout/')

        self.assertEqual(response.status_code, 201)

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order_item.objects.count(), 1)

        self.product.refresh_from_db()

        self.assertEqual(self.product.stock_count, 7)
        self.assertFalse(Cart_item.objects.filter(cart=cart).exists())

    def test_checkout_rejects_empty_cart(self):
        Cart.objects.create(user=self.user)

        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/order/checkout/')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_customer_cannot_update_order_status(self):
        order = Order.objects.create(user=self.user)

        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            f'/api/order/{order.id}/update_status/',
            {'status': 'paid'}
        )

        self.assertEqual(response.status_code, 403)

    def test_admin_can_update_order_status(self):
        order = Order.objects.create(user=self.user)

        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            f'/api/order/{order.id}/update_status/',
            {'status': 'paid'}
        )

        self.assertEqual(response.status_code, 200)

        order.refresh_from_db()

        self.assertEqual(order.status, 'paid')

    def test_invalid_order_status_transition(self):
        order = Order.objects.create(
            user=self.user,
            status='pending'
        )

        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            f'/api/order/{order.id}/update_status/',
            {'status': 'shipped'}
        )

        self.assertEqual(response.status_code, 400)

        order.refresh_from_db()

        self.assertEqual(order.status, 'pending')

    def test_customer_cannot_see_another_users_cart(self):
        other_user = User.objects.create_user(
            username='other',
            password='testpass123'
        )

        Cart.objects.create(user=other_user)

        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/cart/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

    def test_checkout_rejects_insufficient_stock(self):
        cart = Cart.objects.create(user=self.user)

        Cart_item.objects.create(
            cart=cart,
            product=self.product,
            quantity=15
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/order/checkout/')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

        self.product.refresh_from_db()

        self.assertEqual(self.product.stock_count, 10)
        self.assertTrue(
            Cart_item.objects.filter(cart=cart).exists()
        )

    def test_customer_cannot_see_another_users_orders(self):
        other_user = User.objects.create_user(
            username='other',
            password='testpass123'
        )

        Order.objects.create(user=other_user)

        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/order/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

    def test_product_search(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            '/api/product/?search=Laptop'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

