import logging

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.db import transaction

from recipients.models import Recipient

from .models import Notification
from .strategies import get_strategies_map

logger = logging.getLogger(__name__)

# Порядок перебора стратегий отправки уведомлений
STRATEGY_ORDER: tuple[str, ...] = ("email", "telegram", "sms")

# Задержка перед повторной попыткой выполнения задачи (в секундах)
RETRY_DELAY: int = 300

# Максимальное количество автоматических повторов задачи в случае сбоя
MAX_RETRIES: int = 5


def _deliver(notification: Notification, recipient_ids: list[int]) -> list[int]:
    """Прогоняет получателей через failover-цепочку стратегий.

    Args:
        notification: уведомление, задающее тему и текст сообщения.
        recipient_ids: идентификаторы получателей текущей попытки.

    Returns:
        list[int]: id получателей, которым доставить не удалось.
    """
    unnotified_ids = recipient_ids[:]
    strategies = get_strategies_map()
    for strategy_name in STRATEGY_ORDER:
        recipients = Recipient.objects.filter(id__in=unnotified_ids)
        if not recipients.exists():
            break
        strategy = strategies[strategy_name]
        logger.info(f"Strategy {strategy_name}.")
        unnotified_ids = strategy.send(
            subject=notification.topic,
            message=notification.text,
            recipient_list=recipients,
        )
        if not unnotified_ids:
            break
    return unnotified_ids


@shared_task(
    bind=True,
    delivery_mode=2,
    acks_late=True,
    ignore_result=False,
    max_retries=MAX_RETRIES,
)
def send_notification(self, notification_id: int, recipient_ids: list[int]) -> None:
    """Отправляет уведомление получателям с failover и retry.

    Args:
        notification_id: идентификатор уведомления.
        recipient_ids: идентификаторы получателей текущей попытки.

    Raises:
        MaxRetriesExceededError: если ретраи исчерпаны (терминальное состояние).
    """
    unnotified_recipient_ids = recipient_ids[:]

    try:
        with transaction.atomic():
            notification = Notification.objects.get(id=notification_id)
            if notification.status == "CREATED":
                notification.status = "IN_PROGRESS"
                notification.save()
    except Notification.DoesNotExist:
        logger.error(f"Notification {notification_id} not found, stopping task.")
        return

    try:
        unnotified_recipient_ids = _deliver(notification, unnotified_recipient_ids)
    except Exception as e:
        logger.error(f"Notification {notification_id}: unexpected delivery error: {e}.")

    if not unnotified_recipient_ids:
        notification.status = "COMPLETED"
        notification.save()
        logger.warning(f"Notification {notification.topic} completed successfully.")
        return

    try:
        raise self.retry(
            countdown=RETRY_DELAY,
            args=[notification_id, unnotified_recipient_ids],
        )
    except MaxRetriesExceededError:
        logger.error(
            f"Notification {notification_id}: max retries exceeded, giving up."
        )
        raise
