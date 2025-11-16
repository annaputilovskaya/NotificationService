import logging
from abc import ABC, abstractmethod

import requests
from django.core.mail import EmailMessage

from config import settings
from config.settings import EMAIL_HOST_USER, TELEGRAM_URL, TELEGRAM_TOKEN
from notifications.utils import check_email_availability
from recipients.models import Recipient

logger = logging.getLogger(__name__)


class NotificationStrategy(ABC):
    """
    Абстрактный базовый класс для различных стратегии уведомления.
    """
    @abstractmethod
    def send(
        self, subject: str, message: str, recipient_list: list[Recipient]
    ) -> list[int | None]:
        pass


class EmailNotification(NotificationStrategy):
    """
    Уведомление по электронной почте.
    """
    def send(
        self, subject: str, message: str, recipient_list: list[Recipient]
    ) -> list[int | None]:
        results = []
        for recipient in recipient_list:
            try:
                check_email_availability(recipient.email)

                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=EMAIL_HOST_USER,
                    to=[recipient.email],
                )

                sent_count = email.send()

                if sent_count:
                    logger.info(f"Email {subject} sent successfully to {recipient.pk}.")

                else:
                    logger.warning(
                        f"Email {subject} delivery failed to {recipient.pk}."
                    )
                    results.append(recipient.pk)

            except Exception as e:
                logger.error(f"Error sending email {subject} to {recipient.pk}: {e}.")
                results.append(recipient.pk)

        return results


class TelegramNotification(NotificationStrategy):
    """
    Уведомление через телеграм.
    """
    def send(
        self, subject: str, message: str, recipient_list: list[Recipient]
    ) -> list[int | None]:
        results = []
        for recipient in recipient_list:
            tg_chat_id = recipient.tg_chat_id
            if tg_chat_id:

                payload = {
                    "chat_id": tg_chat_id,
                    "text": message,
                }
                try:
                    response = requests.post(
                        f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", data=payload
                    )
                    response.raise_for_status()  # Вызовет исключение при ошибках HTTP (4xx или 5xx)
                    data = response.json()

                    if data.get("ok"):
                        # Сообщение успешно принято сервером Telegram
                        logger.info(
                            f"Telegram message {subject} sent successfully to {recipient.pk}."
                        )

                    else:
                        # Сервер Telegram вернул ошибку, но статус HTTP был 200 OK
                        print(
                            f"Telegram message {subject} delivery failed to {recipient.pk}: {data.get('description')}"
                        )
                        logger.error(
                            f"Telegram message {subject} delivery failed to {recipient.pk}: {data.get('description')}"
                        )
                        results.append(recipient.pk)

                except requests.exceptions.RequestException as e:
                    # Ошибка сети, DNS, таймаут или HTTP-ошибка
                    logger.error(
                        f"Net/HTTP error sending telegram message {subject} to {recipient.pk}: {e}."
                    )
                    results.append(recipient.pk)
                except Exception as e:
                    # Другие непредвиденные ошибки
                    logger.error(
                        f"Unexpected error sending telegram message {subject} to {recipient.pk}: {e}."
                    )
                    results.append(recipient.pk)
            else:
                logger.error(
                    f"Telegram message {subject} delivery failed to {recipient.pk}: there is no tg_chat_id."
                )
                results.append(recipient.pk)

        return results


class SMSNotification(NotificationStrategy):
    """
    Уведомление по СМС.
    """
    def send(
        self, subject: str, message: str, recipient_list: list[Recipient]
    ) -> list[int | None]:
        results = []
        for recipient in recipient_list:
            phone = recipient.phone
            if phone:
                payload = {
                    "api_id": settings.SMS_API_KEY,
                    "to": str(phone),
                    "msg": message.encode("utf-8"),
                    "from": settings.SMS_SENDER,
                    "json": 1,
                    "test": 1,               # TODO: Удалить на продакшене, используется для тестирования сервиса !!!
                }
                try:
                    response = requests.post(
                        "https://sms.ru/sms/send",
                        data=payload,
                    )
                    res = response.json()
                    if res.get("status") == "OK":
                        logger.info(f"SMS {subject} sent successfully to {recipient.pk}.")
                    else:
                        logger.error(
                            f"SMS {subject} delivery failed to {recipient.pk}: {res['sms'].get('status_text')}."
                        )
                        results.append(recipient.pk)

                except requests.exceptions.RequestException as e:
                    # Ошибка сети, DNS, таймаут или HTTP-ошибка
                    logger.error(
                        f"Net/HTTP error sending SMS {subject} to {recipient.pk}: {e}."
                    )
                    results.append(recipient.pk)
                except Exception as e:
                    # Другие непредвиденные ошибки
                    logger.error(
                        f"Unexpected error sending SMS message {subject} to {recipient.pk}: {e}."
                    )
                    results.append(recipient.pk)
            else:
                logger.error(
                    f"SMS {subject} delivery failed to {recipient.pk}: there is no phone."
                )
                results.append(recipient.pk)
        return results


def get_strategies_map():
    """
    Получает стратегии уведомлений.
    """
    return {
        "email": EmailNotification(),
        "telegram": TelegramNotification(),
        "sms": SMSNotification(),
    }
