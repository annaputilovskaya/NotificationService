from django.apps import AppConfig


class RecipientsConfig(AppConfig):
    """
    Конфигурация приложения Django "Получатели".

    Определяет метаданные приложения, такие как используемое поле автоинкремента
    по умолчанию, имя приложения и читаемое человеком название для
    административного интерфейса.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "recipients"
    verbose_name = "Получатели"
