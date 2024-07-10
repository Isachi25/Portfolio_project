from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Reservation
from datetime import datetime, timedelta

@shared_task
def send_reminder_emails():
    now = datetime.now()
    upcoming_reservations = Reservation.objects.filter(
        start_time__gt=now,
        start_time__lt=now + timedelta(hours=1)
    )
    for reservation in upcoming_reservations:
        send_mail(
            'Reservation Reminder',
            f'Reminder: Your reservation for parking spot {reservation.parking_spot} starts at {reservation.start_time}.',
            settings.EMAIL_HOST_USER,
            [reservation.user.email],
            fail_silently=False,
        )
