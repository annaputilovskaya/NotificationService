from rest_framework.serializers import ModelSerializer

from notifications.models import Notification


class NotificationSerializer(ModelSerializer):
    """
    Сериализатор для модели уведомления Notification.

    Используется для преобразования экземпляров модели Notification в формат JSON
    и обратно, а также для валидации данных.
    """

    class Meta:
        """
        Метаданные сериализатора NotificationSerializer.
        """

        model = Notification
        fields = "__all__"
