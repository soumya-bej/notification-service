from .models import Notification, UserPreference
from .queue import push
from .utils import render_template, check_rate_limit


def create_notification(data):
    if not check_rate_limit(data["user_id"]):
        raise Exception("Rate limit exceeded")

    existing = Notification.objects.filter(
        idempotency_key__startswith=data["idempotency_key"]
    ).first()

    if existing:
        print("⚠️ Duplicate request")
        return [existing]

    user_pref = UserPreference.objects.filter(user_id=data["user_id"]).first()

    message = render_template(
        data["message"],
        {"name": "Soumya", "order_id": "123"}
    )

    notifications = []

    for channel in data["channels"]:
        if user_pref and not user_pref.preferences.get(channel, True):
            print(f"❌ Skipped {channel}")
            continue

        notif = Notification.objects.create(
            user_id=data["user_id"],
            message=message,
            channel=channel,
            priority=data["priority"],
            idempotency_key=f"{data['idempotency_key']}_{channel}"
        )

        print(f"✅ Added to Redis queue: {notif.id}")
        push(notif)

        notifications.append(notif)

    return notifications