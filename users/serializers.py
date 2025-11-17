from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """
    Сериализатор пользователя с ограничением информации (минимальный набор полей).

    Используется для предоставления базовой информации о пользователе,
    включая только ID и email.
    """

    class Meta:
        """
        Метаданные сериализатора UserSerializer.
        """

        model = User
        fields = ("id", "email")


class UserDetailSerializer(ModelSerializer):
    """
    Сериализатор профиля пользователя.

    Используется для просмотра и обновления полного профиля пользователя,
    за исключением полей, управляемых автоматически (статусы, даты).
    """

    class Meta:
        """
        Метаданные сериализатора UserDetailSerializer.
        """

        model = User
        fields = "__all__"
        read_only_fields = (
            "id",
            "is_staff",
            "is_superuser",
            "is_active",
            "date_joined",
        )


class UserAdminSerializer(ModelSerializer):
    """
    Сериализатор пользователя для администратора.

    Предоставляет расширенный набор полей для управления пользователем
    администратором, позволяя изменять статусы активности и привилегий,
    но не ID, email или дату регистрации.
    """

    class Meta:
        """
        Метаданные сериализатора UserAdminSerializer.
        """

        model = User
        fields = ("id", "email", "is_staff", "is_superuser", "is_active", "date_joined")
        read_only_fields = ("id", "email", "date_joined")
