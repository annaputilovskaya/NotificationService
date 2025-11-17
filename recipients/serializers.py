from rest_framework.serializers import ModelSerializer

from recipients.models import Recipient


class RecipientSerializer(ModelSerializer):
    """
    Сериализатор для модели получателя Recipient.

    Используется для преобразования экземпляров модели Recipient в формат JSON
    и обратно, а также для валидации данных.
    """

    class Meta:
        """
        Метаданные сериализатора RecipientSerializer.
        """

        model = Recipient
        fields = "__all__"
