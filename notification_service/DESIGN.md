---

# DESIGN.md
# Notification Service - System Design

# Architecture Overview

The system follows a decoupled architecture:

Client → API (Django) → Redis Queue → Worker → Database

---

# Flow

1. Client sends notification request
2. API validates and stores notification in DB
3. Notification pushed to Redis queue
4. Worker consumes from queue asynchronously
5. Notification processed and status updated

---

# Components

# 1. API Layer (Django)
- Handles HTTP requests
- Validates input
- Applies business logic

---

# 2. Service Layer
- Handles core logic
- Applies user preferences
- Implements idempotency

---

# 3. Redis (Queue + Rate Limiting)

# Queue:
- Used as message broker
- Decouples request and processing

# Rate Limiting:
- Uses Redis INCR + EXPIRE
- Limits to 100 requests/hour per user

---

# 4. Worker

- Runs in background
- Processes notifications
- Implements retry logic with exponential backoff

---

# Database Design

# Notification Table

| Field | Description |
|------|-------------|
| id | Primary key |
| user_id | User identifier |
| message | Notification content |
| channel | email/sms/push |
| status | pending/sent/delivered/failed |
| priority | critical/high/normal/low |
| retries | retry count |
| idempotency_key | prevents duplicates |

---

# UserPreference Table

| Field | Description |
|------|-------------|
| user_id | Unique user |
| preferences | JSON (channel settings) |

---

# Retry Mechanism

- Max retries: 3
- Delay: exponential (2^n)
- Ensures reliability

---

# Scalability

- Redis queue allows horizontal scaling
- Multiple workers can process jobs
- Stateless API layer

---

#Reliability

- Persistent DB storage
- Retry mechanism
- Idempotency support

---

# Trade-offs

| Decision | Reason |
|--------|-------|
| SQLite | Simplicity for demo |
| Redis Cloud | No local setup |
| Thread worker | Simple implementation |

---
