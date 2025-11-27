from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {"blank": True, "null": True}


class Recipient(models.Model):
    """
    Модель получателя уведомлений.

    Хранит контактную информацию о пользователях, которые могут получать
    различные типы уведомлений (email, phone, Telegram).

    Attributes:
        first_name (str): Имя получателя. Может быть пустым.
        last_name (str): Фамилия получателя. Может быть пустым.
        email (str): Уникальный адрес электронной почты.
        phone (str): Номер телефона (используется PhoneNumberField). Может быть пустым.
        tg_chat_id (str): Уникальный ID чата Telegram для отправки сообщений. Может быть пустым.
    """

    first_name = models.CharField(max_length=100, verbose_name="Имя", **NULLABLE)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия", **NULLABLE)
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    phone = PhoneNumberField(verbose_name="Телефон", **NULLABLE)
    tg_chat_id = models.CharField(
        max_length=100, verbose_name="ID чата в Telegram", **NULLABLE
    )

    class Meta:
        """
        Метаданные модели Recipient.
        """

        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"

    def __str__(self):
        """
        Возвращает строковое представление объекта (email получателя).

        Returns:
            str: Email получателя.
        """
        return f"{self.email}"
