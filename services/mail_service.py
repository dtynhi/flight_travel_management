from flask import render_template
from flask_mail import Message

from app.extensions import mail
from config.app_config import AppConfig
from utils.logging import _logger


class MailService:
    @staticmethod
    def send_verification_email(email: str, code: str):
        try:
            html_mail_content = render_template("verification_email.html", verification_code=code, user_name=email)
            msg = Message(subject="Verify your email", recipients=[email], html=html_mail_content, sender=AppConfig.MAIL_USERNAME)
            mail.send(msg)
        except Exception as e:
            _logger.error(f"Error while sending email: {str(e)}")
            raise e
