from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_booking_confirmation_template(
    booking: dict,
    email_to: EmailStr,

):
    email = EmailMessage()

    email["Subject"] = "Подтверждение бронирования"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
         f"""
        <html>
            <body>
                <h1>Подтвердите бронирование</h1>
                <p>Вы забронировали отель с {booking["date_from"]} по {booking["date_to"]}</p>
            </body>
        </html>
        """,
        subtype='html'
    )
    return email