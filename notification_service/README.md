# Notification Service (Backend Assignment)

# Overview

This project is a scalable **Notification Service** built using **Django** and **Redis Cloud**.
It supports sending notifications through multiple channels such as Email, SMS, and Push.

The system is designed to be **asynchronous, reliable, and scalable**, using Redis as a message broker and for rate limiting.

---

##  Tech Stack

* **Backend:** Python (Django + Django REST Framework)
* **Queue & Rate Limiting:** Redis Cloud
* **Database:** SQLite (for development)
* **Frontend:** Basic HTML Dashboard

---

# Features

*  Multi-channel notifications (Email, SMS, Push)
*  User preference management (opt-in/opt-out)
*  Priority-based processing (critical → low)
*  Template-based messages (dynamic variables)
*  Delivery tracking (pending, sent, delivered, failed)
*  Retry mechanism with exponential backoff
*  Redis-based asynchronous queue
*  Redis-based rate limiting (100 requests/hour/user)
*  Idempotency support (prevents duplicate notifications)
*  Dashboard for monitoring notifications

---

# Architecture

Client → Django API → Redis Queue → Worker → Database

* API receives request and stores notification
* Notification pushed to Redis queue
* Worker processes notifications asynchronously
* Status updated in database

---

# API Endpoints

# Send Notification

POST `/notifications`

# Get Notification Status

GET `/notifications/{id}`

# Get User Notifications

GET `/users/{userId}/notifications`

# Set User Preferences

POST `/users/{userId}/preferences`

# Get User Preferences

GET `/users/{userId}/preferences/get`

---

#  Setup Instructions (No Virtual Environment)

# 1. Clone Repository

```bash
git clone <your-repo-url>
cd notification_service
```

# 2. Install Dependencies

```bash
pip install django djangorestframework redis
```

# 3. Setup Database

```bash
python manage.py makemigrations
python manage.py migrate
```

---

#  Redis Cloud Setup

1. Create a free Redis Cloud account

2. Create a database

3. Copy:

   * Host
   * Port
   * Username
   * Password

4. Update file:

```
notifications/redis_client.py
```

---

#  Run Application

# Start Django Server

```bash
python manage.py runserver
```

# Start Worker (Separate Terminal)

```bash
python manage.py shell
```

```python
from notifications.worker import start_worker
start_worker()
```

---

#  Testing

Use Postman to test APIs:

1. Set user preferences
2. Send notification
3. Check status
4. Get user notifications

---

#  Dashboard

Open in browser:

```
http://127.0.0.1:8000/dashboard/
```

---

#  Assumptions

* External notification providers (Email/SMS) are mocked
* Authentication is not implemented
* SQLite is used only for development
* Redis Cloud is used instead of local Redis

#  Key Highlights

* Asynchronous processing using Redis queue
* Efficient rate limiting using Redis (INCR + EXPIRE)
* Scalable architecture with worker-based design
* Clean separation of concerns (views, services, worker)

---

# Conclusion

This project demonstrates a production-ready approach to building a **scalable notification system** with asynchronous processing, fault tolerance, and extensibility.

---
