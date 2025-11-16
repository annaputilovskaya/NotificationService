from rest_framework.serializers import ModelSerializer

from notifications.models import Notification


class NotificationSerializer(ModelSerializer):
    """
    Сериализатор уведомления.
    """

    class Meta:
        model = Notification
        fields = "__all__"
