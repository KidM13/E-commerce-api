# E-commerce API

A RESTful e-commerce backend built with **Django REST Framework**. It provides product and category management, shopping cart functionality, order processing, and JWT-based authentication.

## Features

- **Authentication:** JWT-based user authentication.
- **Products & Categories:** Product and category management with staff-only write access.
- **Shopping Cart:** Add products, update quantities, and manage cart items.
- **Checkout:** Create orders, validate stock, reduce inventory, and clear the cart.
- **Order Management:** Track orders and manage status transitions.
- **Permissions:** Role-based access control and customer data isolation.
- **Filtering & Search:** Filter, search, and sort products.
- **Pagination:** Paginated API responses.
- **Throttling:** Request rate limiting.
- **API Documentation:** OpenAPI / Swagger support.
- **Automated Tests:** API tests using DRF's APIClient.

## Project Structure

```text
E-commerce_api/
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── store/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permission.py
│   ├── urls.py
│   └── tests.py
├── manage.py
├── requirements.txt
└── README.md
```

## Technologies

- Python
- Django
- Django REST Framework
- Simple JWT
- django-filter
- drf-spectacular
- SQLite

## API Overview

| Endpoint | Description |
|---|---|
| `/api/category/` | Manage categories |
| `/api/product/` | Browse and manage products |
| `/api/cart/` | Manage shopping carts |
| `/api/cart/add_to_cart/` | Add products to cart |
| `/api/cart-items/` | Manage cart items |
| `/api/order/` | View orders |
| `/api/order/checkout/` | Create an order |
| `/api/order/{id}/update_status/` | Update order status |
| `/api/order-items/` | View order items |
| `/api/token/` | Obtain JWT tokens |
| `/api/token/refresh/` | Refresh JWT tokens |

## API Documentation

This project uses **drf-spectacular** to generate OpenAPI documentation.

The API documentation is available at:

| Documentation | URL | Description |
|---|---|---|
| Swagger UI | `/api/docs/` | Interactive API documentation for exploring and testing endpoints. |
| OpenAPI Schema | `/api/schema/` | Machine-readable API specification in YAML or JSON. |
| ReDoc | `/api/redoc/` | Clean, read-only API documentation for developers. |

### Authentication

The API uses JWT authentication.

1. Obtain an access token using `POST /api/token/`.
2. Open Swagger UI at `/api/docs/`.
3. Click **Authorize**.
4. Enter your access token using the `Bearer` prefix:

   ```text
   Bearer YOUR_ACCESS_TOKEN
   ```

5. You can now test authenticated endpoints through Swagger UI.

## Running Locally

```bash
git clone https://github.com/KidM13/E-commerce-api.git
cd E-commerce_api

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

## Running Tests

```bash
python manage.py test store
```



