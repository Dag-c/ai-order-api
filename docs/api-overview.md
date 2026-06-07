# API Overview

AI Order System API

This document provides a complete reference for all available endpoints in the AI Order System.

The API is built with **FastAPI**, follows REST principles, and uses **JWT authentication** for protected routes.

---

## Base URL

```text
/api/v1
```

---

## Authentication Flow

All protected endpoints require a JWT token in the header:

```text
Authorization: Bearer <token>
```

---

## AUTHENTICATION

### Login

```http
POST /login/
```

Authenticates a user and returns a JWT access token.

Request:

```json
{
  "email": "admin@example.com",
  "password": "securepassword"
}
```

Response:

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

---

## USERS

### Create User

```http
POST /users/
```

Creates a new system user.

Request:

```json
{
  "email": "user@example.com",
  "password": "password123",
  "role": "employee"
}
```

Response:

```json
{
  "message": "User created",
  "user": {
    "id": "uuid",
    "email": "user@example.com"
  }
}
```

---

## PRODUCTS

### Get All Products

```http
GET /products/
```

Returns all available products.

Response:

```json
[
  {
    "id": "uuid",
    "name": "Burger",
    "description": "Cheeseburger",
    "price": 9.99,
    "stock": 10,
    "is_available": true
  }
]
```

---

### Get Product By ID

```http
GET /products/{product_id}
```

---

### Create Product (Admin Only)

```http
POST /products/
```

Creates a new product.

```json
{
  "name": "Pizza",
  "description": "Pepperoni pizza",
  "price": 12.5,
  "stock": 20,
  "is_available": true
}
```

---

### Update Product (Full)

```http
PUT /products/{product_id}
```

---

### Update Product (Partial)

```http
PATCH /products/{product_id}
```

---

### Delete Product

```http
DELETE /products/{product_id}
```

---

## ORDERS

### Get Orders

```http
GET /orders/
```

Supports filters:

- from_date
- to_date
- status
- today

---

### Create Order (Legacy)

```http
POST /orders/
```

---

### Update Order Status

```http
PATCH /orders/{order_id}/status
```

```json
{
  "status": "PREPARING"
}
```

---

## CHAT (AI ORDER ENGINE)

### Chat Endpoint

```http
POST /chat/
```

Core AI-powered ordering endpoint.

Request:

```json
{
  "session_id": "uuid-session",
  "message": "I want 2 burgers and a coke"
}
```

Response:

```json
{
  "intent": "add_items",
  "state": "building_order",
  "cart": [
    {
      "product": "Burger",
      "quantity": 2
    }
  ]
}
```

### Internal Flow

- User message is sent to Gemini
- Intent is extracted
- Products are resolved from DB
- Session is stored in Redis
- State machine updates flow
- Checkout triggers order creation

---

## DASHBOARD

### Summary Metrics

```http
GET /dashboard/summary
```

Returns system KPIs:

```json
{
  "kpis": {
    "total_orders": 120,
    "total_revenue": 2450.50,
    "pending": 10,
    "preparing": 5,
    "delivering": 3
  }
}
```

---

## WEBSOCKETS

### Orders Stream

```text
WS /ws/orders
```

Real-time order updates for admin dashboard.

Event example:

```json
{
  "event": "NEW_ORDER",
  "order_id": "uuid",
  "status": "PENDING"
}
```

Requires JWT authentication via query param or header.

---

## SECURITY

The system implements:

- JWT authentication
- Role-based access control (admin / employee)
- Password hashing (secure storage)
- WebSocket token validation
- Protected admin endpoints

---

## SYSTEM ARCHITECTURE NOTES

This API is part of a larger event-driven system:

- Redis handles session state and Pub/Sub events
- PostgreSQL stores persistent business data
- Gemini processes natural language input
- State machine ensures valid chat flow
- WebSockets enable real-time updates

---

## SUMMARY

This is a production-style backend system demonstrating:

- AI-powered conversational ordering
- Clean REST API design
- Event-driven architecture
- Real-time communication layer
- Scalable session management with Redis
- Modular service-based architecture