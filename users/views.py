from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers import (UserAdminSerializer, UserDetailSerializer,
                               UserSerializer)


class UserCreateAPIView(CreateAPIView):
    """
    Контроллер API для регистрации нового пользователя.

    Предоставляет конечную точку для создания нового пользователя с минимальным
    набором полей (email). Пароль хешируется в сериализаторе.

    Attributes:
        serializer_class (class): Используемый сериализатор (UserSerializer).
        permission_classes (tuple): Разрешения (доступно без аутентификации).
    """

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserListAPIView(ListAPIView):
    """
    Контроллер API для просмотра списка пользователей.

    Предоставляет список всех пользователей с использованием сокращенного
    сериализатора UserSerializer. Требует аутентификации.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)


class UserRetrieveAPIView(RetrieveAPIView):
    """
    Контроллер API для детального просмотра пользователя.

    Позволяет просматривать профиль пользователя. Использует разные сериализаторы
    в зависимости от прав доступа: полный профиль для владельца или суперпользователя,
    сокращенный — для остальных.

    Attributes:
        queryset (QuerySet): Базовый набор данных для поиска пользователя.
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Определяет класс сериализатора в зависимости от прав доступа пользователя.

        Returns:
            class: UserDetailSerializer (для владельца/суперадмина) или UserSerializer (для остальных).
        """
        if self.request.user == self.get_object() or self.request.user.is_superuser:
            return UserDetailSerializer
        return UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    """
    Контроллер API для изменения информации о пользователе.

    Позволяет обновлять профиль пользователя. Использует разные сериализаторы
    и проверяет разрешения:
    - UserDetailSerializer для владельца профиля.
    - UserAdminSerializer для суперпользователя.
    - Иначе вызывает PermissionDenied.

    Attributes:
        queryset (QuerySet): Базовый набор данных для поиска пользователя.
        permission_classes (tuple): Требуемые разрешения (аутентифицирован).
    """

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """
        Определяет класс сериализатора и проверяет разрешения на изменение данных.

        Raises:
            PermissionDenied: Если у пользователя недостаточно прав для редактирования.

        Returns:
            class: Соответствующий класс сериализатора (UserDetailSerializer или UserAdminSerializer).
        """
        if self.request.user == self.get_object():
            return UserDetailSerializer
        if self.request.user.is_superuser:
            return UserAdminSerializer
        raise PermissionDenied("Nor enough permissions.")
