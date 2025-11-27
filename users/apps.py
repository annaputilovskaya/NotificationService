from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Конфигурация приложения Django "Пользователи".

    Определяет метаданные приложения, такие как используемое поле автоинкремента
    по умолчанию, имя приложения и читаемое человеком название для
    административного интерфейса.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "Пользователи"
