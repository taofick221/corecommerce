# CoreCommerce

A production-ready Ecommerce REST API built with Django REST Framework using a scalable Service-Selector architecture. The project includes JWT authentication, Docker, PostgreSQL, Redis, Celery, automated testing, and production-ready best practices.

---

## Features

### Authentication
- JWT Authentication
- User Registration
- User Login
- Token Refresh

### Product Management
- Categories
- Brands
- Products
- Product Variants
- Product Images
- Product Filtering
- Slug-based URLs

### Shopping Cart
- Add to Cart
- Update Cart Items
- Remove Cart Items
- Clear Cart

### Orders
- Create Orders
- Order History
- Order Details
- Stock Validation
- Order Number Generation

### Payments
- Create Payments
- Payment History
- Payment Details
- Payment Status Management

### Coupons
- Coupon Validation
- Percentage Discounts
- Fixed Discounts
- Maximum Discount Limit
- Minimum Order Validation

### Background Tasks
- Order Confirmation Email
- Payment Reminder
- Daily Revenue Report
- Disable Expired Coupons
- Cancel Expired Orders
- Low Stock Notifications

### Security
- JWT Authentication
- API Throttling
- Custom Permissions
- Custom Exception Handling
- Password Validation

---

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Celery Beat
- Docker
- Simple JWT
- drf-spectacular (Swagger/OpenAPI)

---

## Project Structure

```
apps/
│
├── users/
├── products/
├── cart/
├── orders/
├── payments/
├── coupons/
│
core/
config/
```

The project follows a layered architecture using:

- Views
- Serializers
- Services
- Selectors
- Models

---

## API Modules

| Module | Status |
|---------|--------|
| Users | ✅ |
| Products | ✅ |
| Cart | ✅ |
| Orders | ✅ |
| Payments | ✅ |
| Coupons | ✅ |

---

## Installation

### Clone Repository

```bash
git clone https://github.com/taofick221/production-ecommerce-drf.git

cd production-ecommerce-drf
```

---

### Create Environment File

Create a `.env` file.

Example:

```env
DEBUG=True

SECRET_KEY=your_secret_key

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=your_password
```

---

### Run with Docker

```bash
docker compose up --build
```

---

### Apply Migrations

```bash
docker compose exec web python manage.py migrate
```

---

### Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

---

### Run Development Server

```bash
docker compose up
```

---

## API Documentation

Swagger UI

```
http://localhost:8000/api/schema/swagger-ui/
```

OpenAPI Schema

```
http://localhost:8000/api/schema/
```

---

## Running Tests

Run all tests

```bash
docker compose exec web python manage.py test
```

Current Result

```
Ran 281 tests

OK
```

---

## Background Services

Start Celery Worker

```bash
docker compose exec celery celery -A config worker -l info
```

Start Celery Beat

```bash
docker compose exec celery celery -A config beat -l info
```

---

## Main Features

- JWT Authentication
- Dockerized Environment
- PostgreSQL Database
- Redis Cache
- Celery Background Tasks
- Service Layer Architecture
- Selector Layer
- API Throttling
- Custom Exception Handler
- Pagination
- Filtering
- Swagger Documentation
- Automated Testing

---

## Future Improvements

- CI/CD with GitHub Actions
- Coverage Reports
- Payment Gateway Integration
- Wishlist
- Product Reviews
- Inventory Dashboard
- Email Verification

---

## Author

**Md. Taofick Mahmoodur Rahaman**

GitHub

https://github.com/taofick221

LinkedIn

https://www.linkedin.com/in/md-taofick/

Portfolio

https://my-portfolio-website-steel-iota.vercel.app/

---