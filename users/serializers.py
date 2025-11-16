from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """
    Сериализатор пользователя с ограничением информации.
    """

    class Meta:
        model = User
        fields = ("id", "email")


class UserDetailSerializer(ModelSerializer):
    """
    Сериализатор профиля пользователя.
    """

    class Meta:
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
    Серилизатор пользователя для администратора.
    """

    class Meta:
        model = User
        fields = ("id", "email", "is_staff", "is_superuser", "is_active", "date_joined")
        read_only_fields = ("id", "email", "date_joined")
