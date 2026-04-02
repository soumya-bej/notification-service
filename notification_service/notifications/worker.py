import time
import random
from .queue import pop, push
from .models import Notification


def backoff(retries):
    return 2 ** retries


def process(notification):
    print(f" Processing: {notification.id}")

    notification.status = "sent"
    notification.save()

    success = random.choice([True, False])

    if success:
        print(" Delivered")
        notification.status = "delivered"
    else:
        print(" Failed")

        if notification.retries < 3:
            notification.retries += 1
            notification.save()

            delay = backoff(notification.retries)
            print(f" Retry in {delay}s")

            time.sleep(delay)

            push(notification)
            return
        else:
            notification.status = "failed"

    notification.save()


def start_worker():
    print(" Redis Worker started...")

    while True:
        job = pop()

        if job:
            notif = Notification.objects.get(id=job["id"])
            process(notif)