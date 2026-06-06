# AI Order System

AI-powered restaurant ordering platform built with FastAPI, PostgreSQL, Redis, WebSockets, and Google Gemini.

The system allows customers to place orders using natural language conversations while restaurant staff can manage products, monitor orders, and receive real-time notifications.

This project was designed as a portfolio backend application demonstrating:

* REST API development
* JWT authentication and authorization
* AI integration with Google Gemini
* Redis session management
* Event-driven architecture
* Real-time communication with WebSockets
* Dockerized deployment
* PostgreSQL database design

---

## Features

* JWT Authentication
* Role-Based Access Control (Admin / Employee)
* Product Management (CRUD)
* AI-Powered Chat Ordering
* Redis Session Management
* Order Checkout Workflow
* Dashboard Metrics
* Real-Time Notifications using WebSockets
* Redis Pub/Sub Event System
* Dockerized Deployment
* PostgreSQL Persistence
* Google Gemini Integration
* Rate Limiting Protection

---

## Tech Stack

### Backend

* Python 3.12
* FastAPI
* SQLAlchemy
* Pydantic

### Database

* PostgreSQL

### Cache & Messaging

* Redis
* Redis Pub/Sub

### Artificial Intelligence

* Google Gemini API

### Authentication

* JWT Tokens
* Password Hashing (Passlib)

### Deployment

* Docker
* Render

---

## Architecture Overview

Customer
↓
Chat API
↓
Gemini AI
↓
State Machine
↓
Redis Session
↓
Checkout
↓
PostgreSQL
↓
Redis Pub/Sub
↓
WebSocket Dashboard

---

## Main Modules

### Authentication

Handles user login and JWT token generation.

### Product Management

Allows administrators to create, update, delete, and manage menu items.

### AI Chat Ordering

Processes natural language requests and converts them into structured orders.

### Checkout System

Transforms chat session carts into persistent orders and order items.

### Dashboard

Provides KPIs, sales analytics, recent orders, and top-selling products.

### Real-Time Notifications

Uses Redis Pub/Sub and WebSockets to notify connected dashboards when new orders are created.

---

## Security Features

* Password hashing
* JWT authentication
* Role-based authorization
* API rate limiting
* Environment variable configuration
* Protected admin endpoints

---

## Running Locally

### Clone Repository

```bash
git clone <repository-url>
cd ai-order-system
```

### Start Containers

```bash
docker compose -f docker-compose.dev.yml up --build
```

### API Documentation

After startup:

```text
http://localhost:8000/docs
```

---

## Future Improvements

* Async Redis client
* Async SQLAlchemy
* Refresh tokens
* Order pagination
* Automated tests
* CI/CD pipeline
* Kubernetes deployment

---

## Author

Backend portfolio project developed to demonstrate modern Python backend engineering skills using FastAPI, PostgreSQL, Redis, Docker, WebSockets, and AI-powered workflows.
