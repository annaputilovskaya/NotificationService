from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from recipients.models import Recipient
from recipients.serializers import RecipientSerializer


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Контроллер создания получателя."
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Контроллер просмотра списка получателей."
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Контроллер просмотра получателя."
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Контроллер изменения получателя."
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Контроллер частисного изменения получателя."
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Контроллер удаления получателя."
    ),
)
class RecipientViewSet(ModelViewSet):
    """
    ViewSet (Набор представлений) для управления получателями.

    Предоставляет полный набор действий CRUD (Create, Retrieve, Update, Delete)
    для модели Recipient через единый интерфейс.

    Attributes:
        queryset (QuerySet): Базовый набор данных, используемый для всех операций ViewSet'а.
        serializer_class (class): Сериализатор, используемый для обработки данных модели.
        permission_classes (tuple): Требуемые классы разрешений (только для аутентифицированных пользователей).
    """

    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    permission_classes = (IsAuthenticated,)
