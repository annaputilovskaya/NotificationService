from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Сериализатор уведомления. Владелец назначается сервером."""

    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ("owner", "status")
