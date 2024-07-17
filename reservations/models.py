from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
    
class ParkingSpot(models.Model):
    LOCATION_CHOICES = [
        ('A', 'Location A'),
        ('B', 'Location B'),
    ]
    SIZE_CHOICES = [
        ('compact', 'Compact'),
        ('regular', 'Regular'),
        ('electric', 'Electric'),
    ]
    size = models.CharField(max_length=15, choices=SIZE_CHOICES)
    location = models.CharField(max_length=1, choices=LOCATION_CHOICES)
    spot_type = models.CharField(max_length=15)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_location_display()} - {self.size}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    payment_amount = models.DecimalField(max_digits=6, decimal_places=2, editable=False, blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    transaction_code = models.CharField(max_length=3, blank=True, null=True)


    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError('End time must be after start time.')

        overlapping_reservations = Reservation.objects.filter(
            parking_spot=self.parking_spot,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)

        if overlapping_reservations.exists():
            raise ValidationError('This reservation overlaps with another reservation.')

        self.calculate_payment_amount()

    def save(self, *args, **kwargs):
        self.clean()
        self.calculate_payment_amount()  # Ensure payment amount is calculated
        if not self.payment_status:
            raise ValidationError('Payment must be completed before making a reservation.')
        super().save(*args, **kwargs)

    def calculate_payment_amount(self):
        duration = self.end_time - self.start_time
        total_minutes = duration.total_seconds() / 60
        if total_minutes <= 180:
            self.payment_amount = 150
        else:
            extra_minutes = total_minutes - 180
            self.payment_amount = 150 + extra_minutes

    def __str__(self):
        return f"Reservation by {self.user} for {self.parking_spot} from {self.start_time} to {self.end_time}"
    


class Transaction(models.Model):
    code = models.CharField(max_length=10, unique=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.code} - {self.amount}"

