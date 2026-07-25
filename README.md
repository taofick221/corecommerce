<div align="center">

# 🛒 CoreCommerce

### Production-Style Ecommerce REST API built with Django REST Framework

A scalable, production-inspired backend ecommerce application built using **Django REST Framework**. The project follows a clean **Service–Selector Architecture** and integrates **Docker**, **PostgreSQL**, **Redis**, **Celery**, **JWT Authentication**, and **GitHub Actions CI** to demonstrate modern backend engineering practices.

<p>

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.2-success?logo=django)
![DRF](https://img.shields.io/badge/Django_REST_Framework-API-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-Cache-red?logo=redis)
![Celery](https://img.shields.io/badge/Celery-Background_Tasks-green?logo=celery)
![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-black?logo=githubactions)
![Tests](https://img.shields.io/badge/Tests-281_Passing-brightgreen)

</p>

</div>

---

# 📚 Table of Contents

- Overview
- Why CoreCommerce?
- Features
- Tech Stack
- Architecture
- Project Structure
- Installation
- Environment Variables
- Docker Setup
- Running the Project
- API Documentation
- API Endpoints
- Background Tasks
- Testing
- Continuous Integration
- Code Quality
- Project Status
- Future Improvements
- Contributing
- License
- Author

---

# 📖 Overview

CoreCommerce is a production-style Ecommerce REST API designed to demonstrate modern backend development practices using **Django REST Framework**.

Instead of placing business logic inside views or serializers, the project separates responsibilities into dedicated **Service** and **Selector** layers, resulting in a clean, maintainable, and testable architecture.

The application also integrates Docker, PostgreSQL, Redis, Celery, and automated testing to simulate a real-world backend project.

---

# 🎯 Why This Project?

This project was created to practice professional backend engineering concepts including:

- RESTful API Development
- Clean Architecture
- Service–Selector Pattern
- JWT Authentication
- Dockerized Development
- Redis Caching
- Celery Background Processing
- PostgreSQL Database Design
- Automated Testing
- Continuous Integration

The goal is to build software that is easy to maintain, scale, and extend while following industry best practices.

---

# 🚀 Project Highlights

- Production-style Django REST API
- Service–Selector Architecture
- JWT Authentication
- Dockerized Development Environment
- PostgreSQL Database
- Redis Cache
- Celery Background Tasks
- Celery Beat Scheduler
- GitHub Actions CI
- Automated Testing
- Scalable Project Structure
- RESTful API Design

---

# ✨ Features

## 🔐 Authentication

- User Registration
- Secure Login
- JWT Authentication
- Refresh Token
- Protected API Endpoints
- Password Validation

---

## 📦 Product Management

- Categories
- Brands
- Products
- Product Variants
- Product Images
- Slug URLs
- Filtering
- Searching
- Ordering
- Pagination

---

## 🛒 Shopping Cart

- Add Product
- Update Quantity
- Remove Product
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
- Payment Status
- Payment History
- Transaction Tracking

---

## 🎁 Coupons

- Percentage Discount
- Fixed Discount
- Maximum Discount Support
- Minimum Order Validation
- Coupon Validation
- Expiration Validation

---

## ⚙ Background Tasks

Powered by **Celery + Redis**

- Cancel Expired Orders
- Disable Expired Coupons
- Daily Revenue Report
- Email Tasks

---

## 🔒 Security

- JWT Authentication
- API Throttling
- Password Validation
- Custom Permissions
- Custom Exception Handling
# 🏛 Architecture

CoreCommerce follows a layered architecture that separates responsibilities into dedicated components.

```text
                     Client
                        │
                        ▼
               Django REST Views
                        │
                        ▼
                  Serializers
                        │
                        ▼
                    Services
        (Business Logic Layer)
                        │
                        ▼
                   Selectors
        (Database Query Layer)
                        │
                        ▼
                     Models
                        │
                        ▼
                  PostgreSQL

          ▲                         ▲
          │                         │
      Redis Cache             Celery Workers
```

---

# 📁 Project Structure

```text
corecommerce/

├── apps/
│   ├── cart/
│   ├── coupons/
│   ├── orders/
│   ├── payments/
│   ├── products/
│   ├── shipping/
│   └── users/
│
├── config/
│
├── core/
│
├── logs/
│
├── requirements/
│
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── pyproject.toml
├── pytest.ini
└── README.md
```

---

# 🛠 Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python 3.12 |
| Framework | Django 5.2 |
| API | Django REST Framework |
| Database | PostgreSQL |
| Authentication | JWT (SimpleJWT) |
| Cache | Redis |
| Background Tasks | Celery |
| Scheduler | Celery Beat |
| API Documentation | drf-spectacular |
| Containerization | Docker |
| CI | GitHub Actions |
| Testing | Pytest |

---

# 🚀 Getting Started

## 1. Clone Repository

```bash
git clone https://github.com/taofick221/corecommerce.git

cd corecommerce
```

---

## 2. Create Environment Variables

Create a `.env` file in the project root.

Example:

```env
DEBUG=True

SECRET_KEY=your_secret_key

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

REDIS_CACHE_URL=redis://redis:6379/1
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/1

EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=your_password
```

---

## 3. Build Docker Containers

```bash
docker compose up --build
```

---

## 4. Apply Database Migrations

```bash
docker compose exec web python manage.py migrate
```

---

## 5. Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

---

## 6. Start Development Server

```bash
docker compose up
```

Application will be available at:

```
http://localhost:8000/
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

ReDoc

```
http://localhost:8000/api/schema/redoc/
```

---

# 📌 Environment Variables

| Variable | Description |
|-----------|-------------|
| SECRET_KEY | Django Secret Key |
| DEBUG | Enable Debug Mode |
| DB_NAME | PostgreSQL Database |
| DB_USER | PostgreSQL User |
| DB_PASSWORD | PostgreSQL Password |
| DB_HOST | PostgreSQL Host |
| DB_PORT | PostgreSQL Port |
| REDIS_CACHE_URL | Redis Cache URL |
| CELERY_BROKER_URL | Celery Broker |
| CELERY_RESULT_BACKEND | Celery Result Backend |
| EMAIL_HOST_USER | Email Username |
| EMAIL_HOST_PASSWORD | Email Password |

# 🔗 API Endpoints

## 🔐 Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Obtain JWT access & refresh tokens |
| POST | `/api/auth/token/refresh/` | Refresh access token |

---

## 📦 Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List all products |
| GET | `/api/products/{slug}/` | Product details |

Supports:

- Filtering
- Searching
- Ordering
- Pagination

---

## 🛒 Cart

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cart/` | View cart |
| POST | `/api/cart/` | Add product |
| PATCH | `/api/cart/{id}/` | Update quantity |
| DELETE | `/api/cart/{id}/` | Remove cart item |

---

## 📋 Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/orders/` | Create order |
| GET | `/api/orders/` | Order history |
| GET | `/api/orders/{id}/` | Order details |

---

## 💳 Payments

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/payments/` | Create payment |
| GET | `/api/payments/` | Payment history |

---

## 🎁 Coupons

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/coupons/validate/` | Validate coupon |

---

# 🔐 Authentication Flow

CoreCommerce uses **JWT Authentication** via **SimpleJWT**.

```text
User Login
     │
     ▼
Access Token + Refresh Token
     │
     ▼
Authorization Header

Bearer <access_token>
```

Protected endpoints require a valid JWT access token.

---

# ⚡ Background Tasks

Background processing is powered by **Celery** with **Redis** as the message broker.

## Start Celery Worker

```bash
docker compose exec celery celery -A config worker -l info
```

---

## Start Celery Beat

```bash
docker compose exec celery celery -A config beat -l info
```

---

Current scheduled/background tasks include:

- Cancel expired orders
- Disable expired coupons
- Daily revenue report
- Email-related tasks

---

# 🧪 Testing

The project includes automated tests covering:

- Models
- Services
- Selectors
- Serializers
- API Views
- Authentication
- Products
- Cart
- Orders
- Payments
- Coupons
- Permissions
- Filters
- Cache
- API Throttling

Run all tests:

```bash
pytest
```

or

```bash
python -m pytest
```

Latest Result

```text
=============================

281 tests passed

=============================
```

---

# ⚙ Continuous Integration

GitHub Actions automatically executes quality checks on every push and pull request.

Current pipeline includes:

- Black
- isort
- Flake8
- Pytest

This helps ensure code quality and prevents regressions before merging changes.

---

# 📊 Code Quality

The project follows modern Django backend development practices.

## Architecture

- Service Layer
- Selector Layer
- Thin Views
- Reusable Serializers

---

## Database

- PostgreSQL
- Query Optimization
- Model Validation

---

## Performance

- Redis Cache
- Pagination
- Filtering
- Ordering

---

## Development

- Docker
- Environment Variables
- GitHub Actions CI
- Automated Testing
- Layered Architecture

---

# 📌 Project Status

## ✅ Completed Modules

- Authentication
- Products
- Cart
- Orders
- Payments
- Coupons
- Shipping

---

## ✅ Infrastructure

- Docker
- PostgreSQL
- Redis
- Celery
- Celery Beat
- JWT Authentication

---

## ✅ Code Quality

- Layered Architecture
- Service Layer
- Selector Layer
- Automated Testing
- GitHub Actions CI

---

## ✅ Testing Summary

- 281 Automated Tests Passing
- API Tests
- Service Tests
- Selector Tests
- Serializer Tests
- Cache Tests
- Permission Tests
- Filter Tests
- Throttling Tests

---

# 📈 Project Goals

CoreCommerce was developed to practice production-style backend engineering and demonstrate modern Django development techniques.

The project emphasizes:

- Clean Architecture
- Maintainable Code
- Scalable Design
- Testability
- Separation of Concerns
- Containerized Development
- Background Task Processing
- Continuous Integration

---

# 🔮 Future Improvements

The following features are planned for future releases:

- Stripe Payment Integration
- SSLCommerz Integration
- Product Reviews & Ratings
- Wishlist
- Email Verification
- Password Reset via Email
- Social Authentication
- Product Recommendations
- Cloud Storage (AWS S3 / Cloudinary)
- Production Deployment
- Monitoring & Error Tracking

---

# 🤝 Contributing

Contributions are welcome!

If you would like to improve the project:

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/your-feature
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to GitHub

```bash
git push origin feature/your-feature
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute it in accordance with the license.

---

# 👨‍💻 Author

## Md. Taofick Mahmoodur Rahaman

Backend Developer | Django & Django REST Framework

### 🌐 Portfolio

https://my-portfolio-website-steel-iota.vercel.app/

### 💼 LinkedIn

https://www.linkedin.com/in/md-taofick/

### 🐙 GitHub

https://github.com/taofick221

---

# 🙏 Acknowledgements

This project was built for learning, practicing, and demonstrating production-style backend development using Django REST Framework.

Special thanks to the Django and Python open-source communities for providing excellent tools and documentation.

---

# ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub.

Your support helps increase the project's visibility and encourages future improvements.

---

<div align="center">

### Thanks for visiting CoreCommerce!

If you like this project, don't forget to ⭐ the repository.

Happy Coding! 🚀

</div>
