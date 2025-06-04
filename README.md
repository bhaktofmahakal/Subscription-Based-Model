# 🧩 Subscription-Based Microservice

> A modular, RESTful API for managing **subscription plans** and **user subscriptions**, built with **FastAPI**, **PostgreSQL**, and **clean architecture** principles.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.1-brightgreen)](https://fastapi.tiangolo.com/) 
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📚 Table of Contents

- [✨ Features](#-features)
- [🛠️ Tech Stack](#-tech-stack)
- [🏗️ Architecture](#-architecture)
- [📁 Project Structure](#-project-structure)
- [💾 Database Schema](#-database-schema)
- [🔄 API Design](#-api-design)
- [🔐 Authentication & Authorization](#-authentication--authorization)
- [⏱️ Subscription Lifecycle](#-subscription-lifecycle)
- [🚀 Setup Instructions](#-setup-instructions)
- [📝 API Endpoints](#-api-endpoints)
- [💡 Development Approach](#-development-approach)

---

## ✨ Features

- 👤 **User Management**
  - Registration, login, and profile info
  - Role-based access (admin/user)
  - JWT authentication

- 🗂️ **Plan Management**
  - Create/update/delete subscription plans
  - Price, duration, features management

- 📦 **Subscription Management**
  - User subscriptions with upgrade/downgrade
  - History, cancelation, and lifecycle handling

- ⏳ **Automation**
  - Auto-expiry & status transitions
  - Background lifecycle maintenance

- 🔒 **Security & Validation**
  - Pydantic schemas for input validation
  - JWT + bcrypt for secure auth
  - Endpoint-level role protection

---

## 🛠️ Tech Stack

| Layer          | Technology                     |
|----------------|-------------------------------|
| Language       | Python 3.8+                    |
| Framework      | FastAPI                        |
| ORM            | SQLAlchemy 2.0.12              |
| Database       | PostgreSQL / SQLite            |
| Auth           | JWT (python-jose), passlib     |
| Docs           | Swagger UI + ReDoc             |
| Server         | Uvicorn                        |
| Dev Tools      | python-dotenv, email-validator |

---

## 🏗️ Architecture


This project follows a clean architecture pattern with clear separation of concerns:

1. **Presentation Layer** (API Routes)
   - Handles HTTP requests and responses
   - Validates input data
   - Manages authentication and authorization
   - Routes requests to appropriate services

2. **Domain Layer** (Services)
   - Contains business logic
   - Manages subscription lifecycle
   - Handles background tasks
   - Independent of presentation and data layers

3. **Data Layer** (Models & Database)
   - Defines database schema
   - Handles data persistence
   - Provides data access methods
   - Manages relationships between entities

4. **Cross-Cutting Concerns**
   - Authentication and authorization
   - Configuration management
   - Error handling
   - Logging


## 📸 Screenshots

### 🔐 Dashboard Page
![UI Page](image/image.png)



## 📁 Project Structure

```
subscription_service/
├── app/
│   ├── main.py                # FastAPI app entrypoint
│   ├── config.py              # Configuration and environment variables
│   ├── database.py            # Database connection and session management
│   ├── models/                # SQLAlchemy models (database schema)
│   │   ├── __init__.py
│   │   └── models.py          # User, Plan, and Subscription models
│   ├── schemas/               # Pydantic models for request/response validation
│   │   ├── __init__.py
│   │   ├── user.py            # User-related schemas
│   │   ├── plan.py            # Plan-related schemas
│   │   └── subscription.py    # Subscription-related schemas
│   ├── routes/                # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── plans.py           # Plan management endpoints
│   │   └── subscriptions.py   # Subscription management endpoints
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   └── subscription_service.py  # Subscription lifecycle management
│   └── auth/                  # Authentication utilities
│       ├── __init__.py
│       └── jwt.py             # JWT token handling and dependencies
├── .env                       # Environment variables
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## 💾 Database Schema

✅ Modular, readable, and scalable codebase.

---

## 💾 Database Schema

### **Entity Relations**
- One-to-many: `User → Subscriptions`
- One-to-many: `Plan → Subscriptions`
- Many-to-one: `Subscription → (User, Plan)`


The database consists of three main entities:

1. **User**
   - Basic user information (email, username)
   - Authentication details (hashed_password)
   - Role information (is_admin)
   - Account status (is_active)
   - Timestamps (created_at, updated_at)

2. **Plan**
   - Plan details (name, description, features)
   - Pricing information (price)
   - Duration (duration_days)
   - Status (is_active)
   - Timestamps (created_at, updated_at)

3. **Subscription**
   - Relationships to User and Plan
   - Lifecycle information (start_date, end_date)
   - Status (ACTIVE, CANCELLED, EXPIRED)
   - Cancellation details (cancelled_at)
   - Timestamps (created_at, updated_at)

### Entity Relationships:
- A User can have multiple Subscriptions (one-to-many)
- A Plan can be associated with multiple Subscriptions (one-to-many)
- A Subscription belongs to exactly one User and one Plan (many-to-one)


---


## 🔄 API Design

The API follows RESTful conventions with intuitive endpoint design:

- **Resource-based URLs**: Endpoints are organized around resources (users, plans, subscriptions)
- **HTTP Methods**: Proper use of GET, POST, PUT, DELETE for CRUD operations
- **Status Codes**: Appropriate HTTP status codes for different scenarios
- **Query Parameters**: For filtering, pagination, and sorting
- **Path Parameters**: For identifying specific resources
- **Request/Response Bodies**: Consistent JSON structure with proper validation


---


## 🔐 Authentication & Authorization

- **JWT-based Authentication**:
  - Tokens contain user ID, username, and admin status
  - Configurable token expiration
  - Secure password hashing with bcrypt

- **Role-based Authorization**:
  - Regular users can only manage their own subscriptions
  - Admin users can manage all plans and subscriptions
  - Endpoint protection with dependencies

- **Security Features**:
  - Password hashing with salt
  - Token-based authentication
  - CORS middleware configuration


---


## ⏱️ Subscription Lifecycle

Subscriptions follow a defined lifecycle:

1. **Creation**: User subscribes to a plan, creating an ACTIVE subscription
2. **Management**: 
   - User can upgrade/downgrade to different plans
   - Admin can view and manage all subscriptions
3. **Cancellation**: User or admin can cancel a subscription, changing status to CANCELLED
4. **Expiration**: System automatically marks subscriptions as EXPIRED when end_date is reached
5. **Renewal**: User can create a new subscription after cancellation or expiration

---


## 🚀 Setup Instructions

<details>
<summary>Click to view</summary>


### Prerequisites

- Python 3.8+
- PostgreSQL (or SQLite for development)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd subscription-service
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file with the following variables:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/subscription_db
   JWT_SECRET=your_secure_secret_key
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

5. Create the database:
   ```bash
   # In PostgreSQL
   CREATE DATABASE subscription_db;
   ```

### Running the Application

Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

API documentation will be available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc


---



## 📝 API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login to get access token
- `GET /api/v1/auth/me` - Get current user information

### Plans

- `GET /api/v1/plans` - Get all subscription plans
- `GET /api/v1/plans/{plan_id}` - Get a specific plan
- `POST /api/v1/plans` - Create a new plan (admin only)
- `PUT /api/v1/plans/{plan_id}` - Update a plan (admin only)
- `DELETE /api/v1/plans/{plan_id}` - Delete a plan (admin only)

### Subscriptions

- `POST /api/v1/subscriptions` - Create a new subscription
- `GET /api/v1/subscriptions` - Get all subscriptions (admin only)
- `GET /api/v1/subscriptions/user/{user_id}` - Get all subscriptions for a user
- `GET /api/v1/subscriptions/user/{user_id}/active` - Get active subscription for a user
- `GET /api/v1/subscriptions/{subscription_id}` - Get a specific subscription
- `PUT /api/v1/subscriptions/{subscription_id}` - Update a subscription
- `DELETE /api/v1/subscriptions/{subscription_id}` - Cancel a subscription
- `POST /api/v1/subscriptions/check-expired` - Manually check for expired subscriptions (admin only)



---

## 💡 Development Approach

The development of this project followed these key principles:

1. **Modular Design**: The codebase is organized into logical modules with clear responsibilities, making it easy to maintain and extend.

2. **Test-Driven Development**: Key functionality was tested throughout development to ensure reliability.

3. **Iterative Development**: The project was built incrementally, starting with core features and adding more complex functionality over time.

4. **Documentation-First**: API documentation was considered from the beginning, with clear endpoint descriptions and examples.

5. **Security Focus**: Authentication, authorization, and data validation were prioritized throughout development.

6. **Performance Optimization**: Database queries and API endpoints were designed with performance in mind.

7. **Error Handling**: Comprehensive error handling with appropriate HTTP status codes and error messages.


---


### 1. Code Quality
- **Modularity**: Clear separation of concerns with models, schemas, routes, and services
- **Readability**: Consistent naming conventions and code style
- **Best Practices**: Follows FastAPI and SQLAlchemy best practices
- **Error Handling**: Comprehensive error handling with appropriate status codes

### 2. API Design
- **RESTful Conventions**: Proper use of HTTP methods and status codes
- **Intuitive Endpoints**: Logical organization of endpoints around resources
- **Validation**: Input validation with Pydantic schemas
- **Consistency**: Consistent request/response formats

### 3. Documentation
- **API Documentation**: Auto-generated Swagger UI and ReDoc
- **Setup Instructions**: Clear installation and configuration steps
- **Code Comments**: Docstrings and comments explaining complex logic
- **README**: Comprehensive project documentation

### 4. Bonus Features
- **Role-Based Access Control**: Admin and regular user roles with appropriate permissions
- **Subscription Lifecycle Management**: Automatic expiration checks and status updates
- **Background Tasks**: Asynchronous processing for maintenance operations
- **Flexible Configuration**: Environment-based configuration for different deployment scenarios
