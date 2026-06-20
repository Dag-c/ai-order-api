# AI Order System

![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-Cache-red?logo=redis)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

AI-powered restaurant ordering platform built with FastAPI, PostgreSQL, Redis, WebSockets, and Google Gemini.

---

## Overview

AI Order System is a backend platform that allows customers to place restaurant orders using natural language conversations powered by AI.

Instead of selecting items manually, users interact with a chat interface, while the backend interprets intent, manages state, and processes orders in real time.

This project demonstrates modern backend engineering practices, including:

- REST API development
- AI integration with Google Gemini
- Event-driven architecture
- Real-time communication with WebSockets
- Session-based state management
- Scalable service-oriented backend design
- Production-ready Docker deployment

---

## Core Capabilities

- Natural language ordering via AI chat
- Real-time order updates
- Persistent session management with Redis
- Role-based access control (Admin / Employee)
- Admin dashboard with analytics
- Secure JWT authentication
- Rate limiting protection
- Event-driven architecture with Redis Pub/Sub

---

## Features

- JWT Authentication
- Role-Based Access Control
- Product Management (CRUD)
- AI-Powered Chat Ordering System
- Redis Session Storage
- Order Checkout Workflow
- Dashboard Metrics & Analytics
- WebSocket Real-Time Notifications
- Redis Pub/Sub Event System
- PostgreSQL Persistence
- Dockerized Deployment
- Google Gemini Integration
- Rate Limiting Protection

---

## Tech Stack

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic

### Database
- PostgreSQL

### Cache & Messaging
- Redis
- Redis Pub/Sub

### AI Engine
- Google Gemini API

### Authentication
- JWT Tokens
- Password Hashing (Passlib)

### Deployment
- Docker
- Render

---

## Architecture Overview

Client (Chat UI)
↓
FastAPI Chat Endpoint
↓
Gemini AI (Intent Extraction)
↓
Product Resolver (DB Query)
↓
State Machine (Order Flow Control)
↓
Redis Session Storage
↓
Checkout Service
↓
PostgreSQL (Orders Persisted)
↓
Redis Pub/Sub Event
↓
WebSocket Notification System
↓
Admin Dashboard (Real-Time Updates)

---

## How It Works (End-to-End Flow)

1. User sends a message in chat
2. Gemini extracts intent and structured items
3. System resolves products from database
4. Session state is stored in Redis
5. State machine updates conversation flow
6. When ready → checkout is triggered
7. Order is persisted in PostgreSQL
8. Redis publishes order event
9. WebSocket pushes real-time update to dashboard

---

## Main Modules

### Authentication
Handles login, JWT generation, and protected route access.

### Product Management
Admin-only CRUD system for managing menu items.

### AI Chat Ordering
Processes natural language input and converts it into structured order actions.

### Checkout System
Converts chat sessions into persistent orders and order items.

### Dashboard
Provides KPIs, revenue metrics, and order analytics.

### Real-Time Notifications
Uses Redis Pub/Sub + WebSockets for live order updates.

---

## Security Features

- JWT-based authentication
- Role-based authorization (admin / employee)
- Password hashing (secure storage)
- Rate limiting protection (chat endpoint)
- Environment variable configuration
- Protected admin routes

---

## Running Locally

### Clone Repository
```bash
git clone <repository-url>
cd ai-order-system
```

---

### Start with Docker
```bash
docker compose -f docker-compose.dev.yml up --build
```

---

### API Documentation

- Swagger UI: http://localhost:8000/docs  
- OpenAPI: http://localhost:8000/openapi.json  

---

## Documentation

Full system documentation is available in the `/docs` directory:

- [Architecture](docs/architecture.md)
- [Chat Flow](docs/chat-flow.md)
- [API Overview](docs/api-overview.md)
- [Deployment Guide](docs/deployment.md)

---

## Future Improvements

- Async SQLAlchemy migration
- Async Redis client
- Refresh token system
- Unit & integration tests
- CI/CD pipeline (GitHub Actions)
- Kubernetes deployment
- Observability (logs + metrics)

---

## System Highlights

- AI-powered conversational ordering system
- Real-time event-driven backend
- Scalable modular architecture
- Production-ready containerized deployment
- Designed as backend engineering portfolio project

---

## Author

Backend engineering portfolio project designed to demonstrate:

- FastAPI backend architecture
- AI integration systems
- Real-time distributed communication
- Scalable backend design patterns
- Production deployment workflows

## Related Repositories

- Frontend UI: https://github.com/Dag-c/ai-order-web