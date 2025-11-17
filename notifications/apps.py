from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """
    Конфигурация приложения Django "Уведомления".

    Определяет метаданные приложения, такие как используемое поле автоинкремента
    по умолчанию, имя приложения и читаемое человеком название для
    административного интерфейса.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "notifications"
    verbose_name = "Уведомления"
