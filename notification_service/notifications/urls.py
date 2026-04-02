from django.urls import path
from . import views

urlpatterns = [
    path("notifications", views.send_notification),
    path("notifications/<int:id>", views.get_notification),
    path("users/<str:user_id>/notifications", views.user_notifications),
    path("users/<str:user_id>/preferences", views.set_preferences),
    path("users/<str:user_id>/preferences/get", views.get_preferences),
    path("dashboard/", views.dashboard),
]