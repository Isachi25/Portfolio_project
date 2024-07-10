from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('parking_spot', 'user', 'start_time', 'end_time')
    search_fields = ('parking_spot', 'user__username', 'start_time', 'end_time')
    list_filter = ('start_time', 'end_time', 'parking_spot')



