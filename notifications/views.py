from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer
from .tasks import send_notification


class NotificationCreateAPIView(CreateAPIView):
    """Создание уведомления и постановка задачи на отправку."""

    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer) -> None:
        """Сохраняет уведомление владельцем-текущим пользователем и ставит задачу."""
        notification = serializer.save(owner=self.request.user)
        recipient_ids = list(notification.recipients.values_list("id", flat=True))
        send_notification.delay(notification.pk, recipient_ids)


class NotificationRetrieveAPIView(RetrieveAPIView):
    """Просмотр уведомления, принадлежащего текущему пользователю."""

    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Notification.objects.filter(owner=self.request.user)


class NotificationListAPIView(ListAPIView):
    """Список уведомлений текущего пользователя."""

    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Notification.objects.filter(owner=self.request.user)
