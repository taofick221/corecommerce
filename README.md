<div align="center">

# 🛒 CoreCommerce

### Production-Ready Ecommerce REST API built with Django REST Framework

A scalable backend application built using **Django REST Framework**, following a **Service–Selector Architecture** with **Docker**, **PostgreSQL**, **Redis**, **Celery**, **JWT Authentication**, and **281 Automated Tests**.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.x-success?logo=django)
![DRF](https://img.shields.io/badge/DRF-REST_API-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-Cache-red?logo=redis)
![Celery](https://img.shields.io/badge/Celery-Background_Tasks-green?logo=celery)
![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)
![Tests](https://img.shields.io/badge/Tests-281_Passing-brightgreen)

</div>

---

# 📌 Overview

CoreCommerce is a production-style Ecommerce REST API designed using modern backend development practices.

The project emphasizes:

- Clean Architecture
- Service Layer
- Selector Layer
- Background Processing
- Production-ready Docker Environment
- Comprehensive Automated Testing

---

# ✨ Features

## 🔐 Authentication

- JWT Authentication
- User Registration
- User Login
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
- Filtering
- Pagination

---

## 🛒 Cart

- Add to Cart
- Update Cart
- Remove Item
- Clear Cart
- Automatic Total Calculation

---

## 📋 Orders

- Create Order
- Order History
- Order Details
- Stock Validation
- Order Number Generation

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
- Maximum Discount Limit
- Minimum Order Validation

---

## ⚙ Background Tasks

Powered by **Celery + Redis**

- Order Confirmation Email
- Payment Reminder
- Cancel Expired Orders
- Disable Expired Coupons
- Low Stock Notification
- Daily Revenue Report

---

## 🔒 Security

- JWT Authentication
- API Throttling
- Custom Permissions
- Custom Exception Handler
- Password Validation

---

# 🏗 Architecture

The project follows a layered architecture.

```text
Client
   │
   ▼
Views (API)
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
production-ecommerce-drf/

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
| Language | Python |
| Framework | Django |
| API | Django REST Framework |
| Database | PostgreSQL |
| Authentication | JWT (SimpleJWT) |
| Cache | Redis |
| Background Tasks | Celery |
| Scheduler | Celery Beat |
| Documentation | drf-spectacular (Swagger/OpenAPI) |
| Containerization | Docker |

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/taofick221/production-ecommerce-drf.git

cd production-ecommerce-drf
```

---

## Create Environment File

Create a `.env` file.

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

## Run with Docker

```bash
docker compose up --build
```

---

## Apply Migrations

```bash
docker compose exec web python manage.py migrate
```

---

## Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

---

## Run Server

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

# 🧪 Running Tests

Run all tests

```bash
docker compose exec web python manage.py test
```

Current Result

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

# ✅ Production Features

- Dockerized Environment
- PostgreSQL Database
- Redis Cache
- Celery Background Tasks
- JWT Authentication
- Service Layer
- Selector Layer
- API Throttling
- Swagger Documentation
- Automated Testing

---

# 🔮 Future Improvements

- GitHub Actions (CI/CD)
- Test Coverage Report
- Stripe Integration
- SSLCOMMERZ Integration
- Product Reviews
- Wishlist
- Inventory Dashboard
- Email Verification

---

# 👨‍💻 Author

**Md. Taofick Mahmoodur Rahaman**

### GitHub

https://github.com/taofick221

### LinkedIn

https://www.linkedin.com/in/md-taofick/

### Portfolio

https://my-portfolio-website-steel-iota.vercel.app/

---

# ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub.