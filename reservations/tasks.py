from celery import shared_task
from .utils import send_reminder_sms

@shared_task
def send_reminder_sms_task(user_phone, reservation_details):
    send_reminder_sms(user_phone, reservation_details)
