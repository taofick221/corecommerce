<div align="center">

# 🛒 CoreCommerce

### Scalable Ecommerce REST API built with Django REST Framework

A production-style backend application built using **Django REST Framework**, following a clean **Service–Selector Architecture** with **Docker**, **PostgreSQL**, **Redis**, **Celery**, and **JWT Authentication**.

![Python](https://img.shields.io/badge/Python-3.12.13-blue?logo=python)
![Django](https://img.shields.io/badge/Django-6.0.4-success?logo=django)
![DRF](https://img.shields.io/badge/DRF-REST_API-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-Cache-red?logo=redis)
![Celery](https://img.shields.io/badge/Celery-Background_Tasks-green?logo=celery)
![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)
![Tests](https://img.shields.io/badge/Tests-281_Passing-brightgreen)

</div>

---

# 📌 Overview

CoreCommerce is a scalable Ecommerce REST API built with Django REST Framework.

The project follows clean architecture principles by separating business logic into dedicated Service and Selector layers, making the codebase easier to maintain, test, and extend.

It also includes Docker-based development, Redis caching, Celery background processing, JWT authentication, and comprehensive automated testing.

---

# 🚀 Project Highlights

- Clean Service–Selector Architecture
- JWT Authentication
- Dockerized Development Environment
- PostgreSQL Database
- Redis Cache
- Celery Background Tasks
- Swagger / OpenAPI Documentation
- API Throttling
- Comprehensive Automated Testing
- **281 Automated Tests Passing**

---

# ✨ Features

## 🔐 Authentication

- User Registration
- User Login
- JWT Authentication
- Refresh Token
- Password Validation

---

## 📦 Products

- Categories
- Brands
- Products
- Product Variants
- Product Images
- Slug-based URLs
- Product Filtering
- Pagination

---

## 🛒 Cart

- Add Product
- Update Quantity
- Remove Item
- Clear Cart
- Automatic Total Calculation

---

## 📋 Orders

- Create Order
- Order History
- Order Details
- Order Number Generation
- Stock Validation

---

## 💳 Payments

- Create Payment
- Payment History
- Payment Details
- Payment Status Tracking

---

## 🎁 Coupons

- Coupon Validation
- Percentage Discount
- Fixed Discount
- Maximum Discount Support
- Minimum Order Validation

---

## ⚙ Background Tasks

Powered by **Celery + Redis**

- Order Confirmation Email
- Payment Reminder
- Cancel Expired Orders
- Disable Expired Coupons
- Daily Revenue Report
- Low Stock Notification

---

## 🔒 Security

- JWT Authentication
- API Throttling
- Custom Permissions
- Password Validation
- Custom Exception Handler

---

# 🏛 Architecture

The project follows a layered architecture.

```text
Client
   │
   ▼
Views
   │
   ▼
Serializers
   │
   ▼
Services
   │
   ▼
Selectors
   │
   ▼
Models
   │
   ▼
PostgreSQL
```

---

# 📁 Project Structure

```text
corecommerce/

├── apps/
│   ├── users/
│   ├── products/
│   ├── cart/
│   ├── orders/
│   ├── payments/
│   └── coupons/
│
├── config/
├── core/
├── requirements/
├── logs/
│
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── README.md
```

---

# 🛠 Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python 3.12.13 |
| Framework | Django 6.0.4 |
| API | Django REST Framework |
| Database | PostgreSQL |
| Authentication | Simple JWT |
| Cache | Redis |
| Background Tasks | Celery |
| Scheduler | Celery Beat |
| API Documentation | drf-spectacular |
| Containerization | Docker |

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/taofick221/corecommerce.git

cd corecommerce
```

---

## Create Environment File

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

## Build Docker Containers

```bash
docker compose up --build
```

---

## Apply Database Migrations

```bash
docker compose exec web python manage.py migrate
```

---

## Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

---

## Start Development Server

```bash
docker compose up
```

---

# 📖 API Documentation

Swagger UI

```
http://localhost:8000/api/schema/swagger-ui/
```

OpenAPI Schema

```
http://localhost:8000/api/schema/
```

---

# 🧪 Testing

The project includes automated tests for:

- Authentication
- Products
- Cart
- Orders
- Payments
- Coupons
- Services
- Serializers
- Selectors
- API Endpoints

Run all tests:

```bash
docker compose exec web python manage.py test
```

Latest Result

```text
Ran 281 tests

OK
```

---

# 📊 Modules

| Module | Status |
|----------|--------|
| Authentication | ✅ |
| Products | ✅ |
| Cart | ✅ |
| Orders | ✅ |
| Payments | ✅ |
| Coupons | ✅ |

---

# ⚡ Background Workers

Start Celery Worker

```bash
docker compose exec celery celery -A config worker -l info
```

Start Celery Beat

```bash
docker compose exec celery celery -A config beat -l info
```

---

# 🏛 Architecture Principles

The project separates responsibilities into dedicated layers.

- **Models** → Database layer
- **Selectors** → Read/query operations
- **Services** → Business logic
- **Serializers** → Validation & transformation
- **Views** → API endpoints

This architecture improves maintainability, readability, and testability.

---

# 📌 Project Status

✅ Active Development

Completed modules:

- Authentication
- Products
- Cart
- Orders
- Payments
- Coupons

Infrastructure:

- Docker
- PostgreSQL
- Redis
- Celery
- Celery Beat

Quality:

- Layered Architecture
- Service Layer
- Selector Layer
- Comprehensive Automated Tests
- **281 Tests Passing**

---

# 🔮 Future Improvements

- GitHub Actions (CI)
- CD Pipeline
- Test Coverage Reports
- Stripe Integration
- SSLCommerz Integration
- Product Reviews
- Wishlist
- Email Verification
- Admin Dashboard

---

# 👨‍💻 Author

**Md. Taofick Mahmoodur Rahaman**

- 🌐 Portfolio: https://my-portfolio-website-steel-iota.vercel.app/
- 💼 LinkedIn: https://www.linkedin.com/in/md-taofick/
- 🐙 GitHub: https://github.com/taofick221

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.