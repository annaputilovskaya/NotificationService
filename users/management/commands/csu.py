import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда Django management для создания администратора (суперпользователя).

    Создаёт суперпользователя только на основе переменных окружения
    DJANGO_SUPERUSER_EMAIL и DJANGO_SUPERUSER_PASSWORD; если переменные
    не заданы, выводит предупреждение и завершается без создания.
    """

    help = (
        "Создает суперпользователя из переменных окружения "
        "DJANGO_SUPERUSER_EMAIL и DJANGO_SUPERUSER_PASSWORD."
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
            self.stdout.write(
                self.style.WARNING(
                    "DJANGO_SUPERUSER_EMAIL/PASSWORD не заданы — суперпользователь не создан."
                )
            )
            return

        # Прерываем выполнение команды, если пользователь с таким email уже есть
        if User.objects.filter(email=email).exists():
            return

        # Создаем пользователя
        User.objects.create_superuser(email=email, password=password)
