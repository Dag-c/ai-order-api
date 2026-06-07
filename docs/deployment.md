# Deployment Guide

AI Order System - Deployment Documentation

This guide explains how to run, configure, and deploy the AI Order System in both local and production environments.

---

## 1. System Requirements

Before running the system, ensure you have installed:

- Python 3.12+
- Docker & Docker Compose
- PostgreSQL
- Redis
- Git

---

## 2. Environment Variables

Create a `.env` file in the root directory:

```env
ENV=development

# DATABASE
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_order_db

# AUTH
SECRET_APP_KEY=your_secret_key
ALGORITHM=HS256

# REDIS
REDIS_URL=redis://redis:6379
SESSION_TTL_SECONDS=3600

# AI
GEMINI_API_KEY=your_gemini_key

# CORS
CORS_ORIGINS=http://localhost:3000
```

---

## 3. Local Development (Docker)

### Build and start services

```bash
docker-compose -f docker-compose.dev.yml up --build
```

---

### Services available

| Service      | URL |
|--------------|-----|
| FastAPI API  | http://localhost:8000 |
| PostgreSQL   | localhost:5432 |
| Redis        | localhost:6379 |

---

### API Documentation

Once running:

- Swagger UI: http://localhost:8000/docs  
- OpenAPI JSON: http://localhost:8000/openapi.json  

---

## 4. Production Deployment (Docker)

### Build image

```bash
docker build -t ai-order-system .
```

---

### Run container

```bash
docker run -p 10000:10000 \
  --env-file .env \
  ai-order-system
```

---

## 5. Deploy on Render

### Requirements

- GitHub repository connected
- Environment variables configured in Render dashboard

### Build command

```bash
pip install -r requirements.txt
```

### Start command

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## 6. Database Setup (PostgreSQL)

The system requires a running PostgreSQL instance.

On startup, the application will:

- Validate connection (`SELECT 1`)
- Initialize schema (if configured)
- Ensure database readiness before serving traffic

---

## 7. Redis Setup

Redis is used for:

- Chat session storage
- State machine persistence
- Pub/Sub event system
- WebSocket real-time updates

Default connection:

```text
redis://redis:6379
```

---

## 8. Health Check

```http
GET /health
```

Returns system status:

- API availability
- Database connectivity
- Redis connectivity

Used for monitoring and deployment validation.

---

## 9. Common Issues

### Database connection failed
- Verify credentials
- Ensure PostgreSQL is running
- Check network access (Docker vs local)

---

### Redis connection error
- Confirm Redis container is running
- Validate `REDIS_URL`

---

### Gemini API errors
- Check API key validity
- Verify quota limits (free tier is limited)

---

## 10. System Architecture Summary

The system is composed of:

- FastAPI (API layer)
- PostgreSQL (persistent storage)
- Redis (session + event system)
- Google Gemini (AI processing)
- WebSockets (real-time updates)
- Docker (deployment layer)

---

## 11. Final Notes

This deployment setup is designed to support:

- AI-powered conversational ordering
- Real-time event-driven architecture
- Stateless API with Redis session management
- Scalable production deployment model