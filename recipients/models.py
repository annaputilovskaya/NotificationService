from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {"blank": True, "null": True}


class Recipient(models.Model):
    """
    Модель получателя.
    """

    first_name = models.CharField(max_length=100, verbose_name="Имя", **NULLABLE)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия", **NULLABLE)
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    phone = PhoneNumberField(verbose_name="Телефон", **NULLABLE)
    tg_chat_id = models.CharField(
        max_length=100, verbose_name="ID чата в Telegram", **NULLABLE
    )

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"

    def __str__(self):
        return f"{self.email}"
