from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer
from .tasks import send_notification


class NotificationCreateAPIView(CreateAPIView):
    """
    Контроллер API для создания нового уведомления.

    Предоставляет конечную точку для создания уведомления. После успешного
    создания запускает асинхронную задачу Celery на отправку этого уведомления.

    Attributes:
        serializer_class (class): Сериализатор, используемый для валидации и десериализации данных.
        permission_classes (tuple): Требуемые классы разрешений (только для аутентифицированных).
    """

    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """
        Сохраняет новый объект уведомления и запускает фоновую задачу отправки.

        Args:
            serializer (NotificationSerializer): Экземпляр сериализатора с валидными данными.
        """
        notification = serializer.save()

        recipient_ids = list(notification.recipients.values_list("id", flat=True))
        send_notification.delay(notification.pk, recipient_ids)


class NotificationRetrieveAPIView(RetrieveAPIView):
    """
    Контроллер API для просмотра деталей конкретного уведомления.

    Предоставляет конечную точку для получения информации по одному уведомлению
    по его PK/ID.
    """

    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Notification.objects.all()


class NotificationListAPIView(ListAPIView):
    """
    Контроллер API для просмотра списка всех уведомлений.

    Предоставляет конечную точку для получения списка всех доступных уведомлений.
    """

    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Notification.objects.all()
