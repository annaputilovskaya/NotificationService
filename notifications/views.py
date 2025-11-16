from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer
from .tasks import send_notification


class NotificationCreateAPIView(CreateAPIView):
    """
    Контроллер создания уведомления.
    """

    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):

        notification = serializer.save()

        recipient_ids = list(notification.recipients.values_list("id", flat=True))
        send_notification.delay(notification.pk, recipient_ids)


class NotificationRetrieveAPIView(RetrieveAPIView):
    """
    Контроллер просмотра уведомления.
    """

    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Notification.objects.all()


class NotificationListAPIView(ListAPIView):
    """
    Контроллер просмотра списка уведомлений.
    """

    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Notification.objects.all()
