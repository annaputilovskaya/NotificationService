import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда Django management для создания администратора (суперпользователя).

    Позволяет создать суперпользователя на основе переменных окружения
    DJANGO_SUPERUSER_EMAIL и DJANGO_SUPERUSER_PASSWORD, или используя
    значения по умолчанию, если переменные не заданы.
    """

    help = (
        "Создает суперпользователя из переменных окружения или значений по умолчанию."
    )

    def handle(self, *args, **kwargs):
        """
        Логика выполнения команды создания суперпользователя.

        Args:
            *args: Позиционные аргументы команды (не используются).
            **kwargs: Именованные аргументы команды (не используются).
        """

        # Получаем значения из переменных окружения
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        if not email or not password:
            email = "admin@admin.com"
            password = "admin-01"

        # Прерываем выполнение команды, если пользователь с таким email уже есть
        if User.objects.filter(email=email).exists():
            return

        # Создаем пользователя
        user = User.objects.create(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
