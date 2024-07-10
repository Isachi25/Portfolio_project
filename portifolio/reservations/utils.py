from twilio.rest import Client
from django.conf import settings

def send_sms(to, body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to
    )
    return message.sid

def send_confirmation_sms(user_phone, reservation_details):
    body = f'Your reservation is confirmed: {reservation_details}'
    send_sms(user_phone, body)

def send_reminder_sms(user_phone, reservation_details):
    body = f'Reminder: Your reservation is coming up: {reservation_details}'
    send_sms(user_phone, body)
