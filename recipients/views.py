from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from recipients.models import Recipient
from recipients.serializers import RecipientSerializer


class RecipientViewSet(ModelViewSet):
    """
    Контроллер получателя.
    """

    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    permission_classes = (IsAuthenticated,)
