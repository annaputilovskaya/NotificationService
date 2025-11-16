import logging
from abc import ABC, abstractmethod

from django.core.mail import EmailMessage

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