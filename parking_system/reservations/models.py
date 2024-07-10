from django.db import models
from django.contrib.auth.models import User

class ParkingSpot(models.Model):
    spot_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.spot_number

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f'{self.user} - {self.parking_spot} ({self.start_time} to {self.end_time})'

    class Meta:
        unique_together = ('parking_spot', 'start_time', 'end_time')
