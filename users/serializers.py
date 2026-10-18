from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации/краткой информации о пользователе."""

    password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ("id", "email", "password")

    def create(self, validated_data) -> User:
        """Создаёт пользователя с хешированным паролем."""
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """Полный профиль пользователя без поля пароля."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
        )
        read_only_fields = (
            "id",
            "is_staff",
            "is_superuser",
            "is_active",
            "date_joined",
            "last_login",
        )


class UserAdminSerializer(serializers.ModelSerializer):
    """Сериализатор управления пользователем администратором."""

    class Meta:
        model = User
        fields = ("id", "email", "is_staff", "is_superuser", "is_active", "date_joined")
        read_only_fields = ("id", "email", "date_joined")
