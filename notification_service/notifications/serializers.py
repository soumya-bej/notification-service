from rest_framework import serializers
from .models import Notification


class NotificationCreateSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    message = serializers.CharField()
    channels = serializers.ListField(child=serializers.CharField())
    priority = serializers.CharField()
    idempotency_key = serializers.CharField()


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"