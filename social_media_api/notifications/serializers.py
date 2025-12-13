from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source="actor.username")

    class Meta:
        model = Notification
        fields = [
            "id",
            "actor",
            "actor_username",
            "verb",
            "object_id",
            "read",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "actor",
            "actor_username",
            "verb",
            "object_id",
            "created_at",
        ]
