from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers import UserSerializer, UserDetailSerializer, UserAdminSerializer


class UserCreateAPIView(CreateAPIView):
    """
    Контроллер регистрации пользователя.
    """

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """
    Контроллер списка пользователей.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)


class UserRetrieveAPIView(RetrieveAPIView):
    """
    Контроллер детального просмотра пользователя.
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Проверяет, какой объем информации о пользователе может просматривать текущий пользователь.
        """
        if self.request.user == self.get_object() or self.request.user.is_superuser:
            return UserDetailSerializer
        return UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    """
    Контроллер изменения информации о пользователе.
    """

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """
        Проверяет, какие данные о пользователе может изменять текущий пользователь.
        """
        if self.request.user == self.get_object():
            return UserDetailSerializer
        if self.request.user.is_superuser:
            return UserAdminSerializer
        raise PermissionDenied("Nor enough permissions.")
