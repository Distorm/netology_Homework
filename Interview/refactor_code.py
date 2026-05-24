import email
import smtplib
import imaplib
from email.message import Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


LOGIN = "test123"
PASSWORD = "12345676"
USER_EMAIL = "test123@gmail.com"


class EmailClient:

    def __init__(
            self,
            login: str,
            password: str,
            smtp_server: str = "smtp.gmail.com",
            smtp_port: int = 587,
            imap_server: str = "imap.gmail.com",
            imap_port: int = 993,
    ) -> None:
        self.login = login
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.imap_server = imap_server
        self.imap_port = imap_port

    def send_message(
            self,
            recipients: list[str],
            subject: str,
            body: str,
    ) -> None:
        msg = MIMEMultipart()
        msg["From"] = self.login
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()  # Шифрование TLS
                server.ehlo()
                server.login(self.login, self.password)
                server.sendmail(self.login, recipients, msg.as_string())
        except smtplib.SMTPException as error:
            print(f"Ошибка SMTP при отправке письма: {error}")
            raise

    def get_latest_message(self, subject_filter: str | None = None) -> Message | None:
        mail = None
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.login, self.password)
            mail.select("inbox")

            criterion = f'(HEADER Subject "{subject_filter}")' if subject_filter else "ALL"
            result, data = mail.uid("search", None, criterion)

            if result != "OK" or not data[0]:
                print("Письма не найдены.")
                return None

            latest_email_uid = data[0].split()[-1]
            result, data = mail.uid("fetch", latest_email_uid, "(RFC822)")

            if result != "OK":
                print("Не удалось получить текст письма.")
                return None

            raw_email = data[0][1]
            return email.message_from_bytes(raw_email)

        except imaplib.IMAP4.error as error:
            print(f"Ошибка IMAP: {error}")
            return None
        finally:
            if mail is not None:
                try:
                    mail.logout()
                except Exception:
                    pass


if __name__ == "__main__":

    client = EmailClient(
        login=LOGIN,
        password=PASSWORD,
    )

    recipients_list = ["vasya@email.com", "petya@email.com", USER_EMAIL]
    subject_text = "Тестовая тема"
    message_body = "Привет! Это тестовое сообщение после рефакторинга."

    print("Попытка отправки письма...")
    try:
        client.send_message(
            recipients=recipients_list,
            subject=subject_text,
            body=message_body,
        )
        print("✅ Письмо успешно отправлено.")
    except Exception:
        print("❌ Не удалось отправить письмо.")

    print("\nПопытка получения письма...")
    received_msg = client.get_latest_message(subject_filter=subject_text)

    if received_msg:
        print(f"✅ Получено письмо от: {received_msg.get('From')}")
        print(f"Тема: {received_msg.get('Subject')}")
    else:
        print("❌ Письмо не найдено или произошла ошибка.")