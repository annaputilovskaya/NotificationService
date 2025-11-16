import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда создания администратора (суперпользователя).
    """

    def handle(self, *args, **kwargs):

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
