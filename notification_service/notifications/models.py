from django.db import models

# Create your models here.

class Notification(models.Model):
    STATUS = [
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("delivered", "Delivered"),
        ("failed", "Failed"),
    ]

    PRIORITY = [
        ("critical", "Critical"),
        ("high", "High"),
        ("normal", "Normal"),
        ("low", "Low"),
    ]

    user_id = models.CharField(max_length=100)
    message = models.TextField()
    channel = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    priority = models.CharField(max_length=20, choices=PRIORITY)
    retries = models.IntegerField(default=0)
    idempotency_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserPreference(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    preferences = models.JSONField(default=dict)


class RateLimit(models.Model):
    user_id = models.CharField(max_length=100)
    count = models.IntegerField(default=0)
    last_reset = models.DateTimeField(auto_now_add=True)