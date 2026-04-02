from django.shortcuts import render

# Create your views here.
import threading
from.worker import start_worker
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import Notification, UserPreference
from .serializers import NotificationSerializer, NotificationCreateSerializer
from .services import create_notification


@api_view(["POST"])
def send_notification(request):
    serializer = NotificationCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        notifs = create_notification(serializer.validated_data)
    except Exception as e:
        return Response({"error": str(e)}, status=429)

    return Response(NotificationSerializer(notifs, many=True).data)


@api_view(["GET"])
def get_notification(request, id):
    notif = Notification.objects.filter(id=id).first()
    return Response(NotificationSerializer(notif).data)


@api_view(["GET"])
def user_notifications(request, user_id):
    notifs = Notification.objects.filter(user_id=user_id)
    return Response(NotificationSerializer(notifs, many=True).data)


@api_view(["POST"])
def set_preferences(request, user_id):
    pref, _ = UserPreference.objects.get_or_create(user_id=user_id)
    pref.preferences = request.data.get("preferences", {})
    pref.save()
    return Response({"message": "updated"})


@api_view(["GET"])
def get_preferences(request, user_id):
    pref = UserPreference.objects.filter(user_id=user_id).first()
    return Response(pref.preferences if pref else {})


def dashboard(request):
    notifications = Notification.objects.all().order_by("-created_at")
    preferences = UserPreference.objects.all()

    return render(request, "dashboard.html", {
        "notifications": notifications,
        "preferences": preferences
    })



#To start the worker in background thread
def start_background_worker():
    thread = threading.Thread(target=start_worker, daemon=True)
    thread.start()
start_background_worker()
