from rest_framework.serializers import ModelSerializer

from recipients.models import Recipient


class RecipientSerializer(ModelSerializer):
    """
    Сериализатор получателя.
    """

    class Meta:
        model = Recipient
        fields = "__all__"
