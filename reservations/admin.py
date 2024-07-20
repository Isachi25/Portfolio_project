from django.contrib import admin
from .models import ParkingSpot, Reservation, Profile, Transaction
# Register your models here.

admin.site.register(ParkingSpot)
admin.site.register(Reservation)
admin.site.register(Profile)
admin.site.register(Transaction)


