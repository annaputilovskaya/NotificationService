from django.contrib import admin

from notifications.models import Notification


class RecipientInline(admin.TabularInline):
    """
    Встроенный (inline) интерфейс администратора для управления получателями уведомлений.

    Этот класс предоставляет табличный интерфейс внутри NotificationAdmin
    для добавления и удаления получателей через промежуточную модель
    отношения many-to-many 'recipients'.
    """

    model = Notification.recipients.through


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Конфигурация административного интерфейса для модели Notification.

    Определяет, как экземпляры модели Notification отображаются и управляются
    в интерфейсе администратора Django, включая поля отображения списка
    и использование RecipientInline для управления связанными пользователями.

    Attributes:
        list_display (tuple): Поля, отображаемые в списке объектов в админке.
    """

    list_display = (
        "pk",
        "topic",
        "text",
        "status",
    )
    inlines = [RecipientInline]
