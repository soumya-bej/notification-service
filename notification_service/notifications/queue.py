import json
from .redis_client import redis_client

QUEUE_NAME = "notification_queue"


def push(notification):
    data = {
        "id": notification.id,
        "priority": notification.priority
    }

    redis_client.lpush(QUEUE_NAME, json.dumps(data))


def pop():
    data = redis_client.brpop(QUEUE_NAME, timeout=5)

    if data:
        return json.loads(data[1])

    return None