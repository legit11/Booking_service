import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery import celery
from app.tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_picture(
        path: str,

):
    img_path = Path(path)
    img = Image.open(img_path)
    img_resized_1000_500 = img.resize((1000, 500))
    img_resized_200_100 = img.resize((200, 100))
    img_resized_1000_500.save(f"app/static/images/resized_1000_500_{img_path.stem}.jpg", format="JPEG")
    img_resized_200_100.save(f"app/static/images/resized_200_100_{img_path.stem}.jpg", format="JPEG")


@celery.task
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr,
):
    email_to_mock = settings.SMTP_USER
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(email_to_mock, settings.SMTP_PASS)
        server.send_message(msg_content)

