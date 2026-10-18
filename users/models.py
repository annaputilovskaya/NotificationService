from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

NULLABLE = {"blank": True, "null": True}


class UserManager(BaseUserManager):
    """Менеджер пользователей с email в качестве логина."""

    def _create_user(
        self, email: str, password: str | None, **extra_fields
    ) -> "User":
        if not email:
            raise ValueError("Email обязателен.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, password: str | None = None, **extra_fields
    ) -> "User":
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Модель пользователя.

    Расширяет стандартную модель пользователя Django (AbstractUser),
    используя адрес электронной почты в качестве основного уникального
    идентификатора (логина) вместо имени пользователя (username).

    Attributes:
        email (str): Уникальный адрес электронной почты пользователя, используется как логин.
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Электронная почта")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        """
        Метаданные модели User.
        """

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
