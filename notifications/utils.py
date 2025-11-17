import smtplib
import socket

import dns.resolver

from config.settings import EMAIL_HOST_USER


def check_email_availability(email, sender_email=EMAIL_HOST_USER, timeout=10):
    """
    Проверяет доступность email-адреса, пытаясь подключиться к его SMTP-серверу
    и проверить получателя (RCPT TO).

    Args:
        email (str): Проверяемый email-адрес получателя.
        sender_email (str): Email-адрес отправителя (используется в команде MAIL FROM).
        timeout (int): Таймаут ожидания сетевых операций в секундах.

    Raises:
        Exception: В случае, если домен не имеет MX-записей, не существует,
                  или SMTP-сервер отклоняет адрес получателя.

    Returns:
        None: Если email-адрес признан доступным и действительным.
    """

    domain = email.split("@")[1]
    # Установка общего таймаута для всех операций с сокетами
    socket.setdefaulttimeout(timeout)

    try:
        # Получаем MX-записи домена
        records = dns.resolver.resolve(domain, "MX")
        mx_record = records[0].exchange.to_text()

        # Попытка подключения к SMTP-серверу через порт 25 (стандартный)
        try:
            server = smtplib.SMTP(mx_record, 25, timeout=timeout)
            server.set_debuglevel(0)
            code, message = server.helo("localhost")
            if code not in [250, 251]:
                raise Exception(f"HELO failed with code {code}: {message.decode()}")

            # Отправка команды RCPT TO
            server.mail(sender_email)
            code, message = server.rcpt(str(email))

            if code in [250, 251, 252]:
                return

            raise Exception(
                f"Email is likely invalid/unavailable. Code {code}: {message.decode()}"
            )

        except smtplib.SMTPConnectError as e:
            # Попытка подключения через порт 587 с STARTTLS
            server = smtplib.SMTP(mx_record, 587, timeout=timeout)
            server.set_debuglevel(0)
            server.ehlo()
            if server.ehlo()[0] >= 200:
                server.starttls()
                server.ehlo()
                server.mail(sender_email)
                code, message = server.rcpt(str(email))
                if code == 250:
                    return
                raise Exception(f"Email check failed using STARTTLS.")

        except Exception as e:
            return f"Произошла ошибка при работе с SMTP-сервером: {e}"
        finally:
            if "server" in locals() and server:
                server.quit()

    except dns.resolver.NoMXSError:
        raise Exception("Домен не имеет MX-записей.")
    except dns.resolver.NXDOMAIN:
        raise Exception("Домен не существует.")
    except Exception as e:
        raise Exception(f"Произошла ошибка при разрешении DNS или другая ошибка: {e}")
