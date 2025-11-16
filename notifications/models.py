from django.db import models

from recipients.models import Recipient

NULLABLE = {"blank": True, "null": True}


class Notification(models.Model):
    """Модель уведомления."""

    STATUS_CHOICES = [
        ("CREATED", "Создано"),
        ("IN_PROGRESS", "В процессе"),
        ("COMPLETED", "Завершено"),
    ]

    topic = models.CharField(max_length=250, verbose_name="Тема", **NULLABLE)
    text = models.TextField(verbose_name="Текст", **NULLABLE)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default="CREATED", verbose_name="Статус"
    )
    recipients = models.ManyToManyField(
        Recipient, verbose_name="Получатели",  **NULLABLE
    )

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
