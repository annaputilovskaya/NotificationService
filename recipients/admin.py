from django.contrib import admin

from recipients.models import Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    """
    Конфигурация административного интерфейса для модели Recipient.

    Определяет, как получатели (Recipient) отображаются и управляются
    в интерфейсе администратора Django.

    Attributes:
        list_display (tuple): Поля, отображаемые в списке объектов в админке.
    """

    list_display = (
        "pk",
        "first_name",
        "last_name",
        "email",
        "phone",
        "tg_chat_id",
    )
