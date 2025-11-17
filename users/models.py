from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


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

    class Meta:
        """
        Метаданные модели User.
        """

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
