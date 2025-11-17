from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Конфигурация административного интерфейса для модели User (Пользователь).

    Определяет, как пользователи отображаются и управляются в интерфейсе
    администратора Django.

    Attributes:
        list_display (tuple): Поля, отображаемые в списке объектов в админке.
    """

    list_display = (
        "pk",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
    )
