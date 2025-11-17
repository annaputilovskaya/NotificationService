from django.db import models

from recipients.models import Recipient

NULLABLE = {"blank": True, "null": True}


class Notification(models.Model):
    """
    Модель уведомления.

    Определяет структуру данных для хранения информации об отправляемых
    уведомлениях, включая тему, текст, статус и список получателей.

    Attributes:
        topic (str): Тема уведомления. Может быть пустым.
        text (str): Текст сообщения уведомления. Может быть пустым.
        status (str): Текущий статус уведомления (CREATED, IN_PROGRESS, COMPLETED).
        recipients (ManyToManyField): Связь many-to-many с получателями уведомления.
    """

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
        Recipient, verbose_name="Получатели", **NULLABLE
    )

    class Meta:
        """
        Метаданные модели Notification.
        """

        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        """
        Возвращает строковое представление объекта (тему уведомления).

        Returns:
            str: Тема уведомления.
        """
        return self.topic
