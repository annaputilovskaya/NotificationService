import logging
from celery import shared_task
from django.db import transaction

from recipients.models import Recipient
from .models import Notification
from .strategies import get_strategies_map

logger = logging.getLogger(__name__)

STRATEGY_ORDER = ("email", "telegram", "sms")
RETRY_DELAY = 300


@shared_task(bind=True, delivery_mode=2, acks_late=True, ignore_result=False)
def send_notification(
    self,
    notification_id: int,
    recipient_ids: list[int],
):
    unnotified_recipient_ids = recipient_ids[:]
    try:
        # Получаем уведомление из БД
        with transaction.atomic():
            notification = Notification.objects.get(id=notification_id)
            # Меняем статус уведомления при взятии в работу
            if notification.status == "CREATED":
                notification.status = "IN_PROGRESS"
                notification.save()

        # Перебираем стратегии
        strategy_id = 0
        while strategy_id < len(STRATEGY_ORDER):
            strategy = get_strategies_map()[STRATEGY_ORDER[strategy_id]]
            logger.info(f"Strategy {STRATEGY_ORDER[strategy_id]}.")

            # Получаем объекты Recipient для текущего списка пользователей
            recipients = Recipient.objects.filter(id__in=unnotified_recipient_ids)
            if not recipients.exists():
                break

            unnotified_recipient_ids = strategy.send(
                subject=notification.topic,
                message=notification.text,
                recipient_list=recipients,
            )

            if not unnotified_recipient_ids:
                break

            strategy_id += 1

        # Переводим успешно отправленное уведомление в статус завершенного
        if not unnotified_recipient_ids:
            notification.status = "COMPLETED"
            notification.save()
            logger.warning(f"Notification {notification.topic} completed successfully.")
        # Повторяем попытку после задержки
        else:
            raise self.retry(
                countdown=RETRY_DELAY,
                args=[notification_id, unnotified_recipient_ids],
                exc=Exception(
                    f"Failed delivery to {len(unnotified_recipient_ids)} recipients across all channels."
                ),
            )
    except Notification.DoesNotExist:
        logger.error(f"Notification {notification_id} not found, stopping task.")
    except Exception as e:
        raise self.retry(
            exc=e,
            countdown=RETRY_DELAY,
            args=[notification_id, unnotified_recipient_ids],
        )
