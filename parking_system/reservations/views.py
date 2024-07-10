from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ParkingSpot, Reservation
from .forms import ReservationForm
from django.core.mail import send_mail
from django.conf import settings

@login_required
def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            # Check for double booking
            if Reservation.objects.filter(
                parking_spot=reservation.parking_spot,
                start_time__lt=reservation.end_time,
                end_time__gt=reservation.start_time
            ).exists():
                messages.error(request, 'This parking spot is already reserved for the selected time period.')
            else:
                reservation.save()
                messages.success(request, 'Reservation made successfully!')
                # Send confirmation email
                send_mail(
                    'Reservation Confirmation',
                    f'Your reservation for parking spot {reservation.parking_spot} from {reservation.start_time} to {reservation.end_time} has been confirmed.',
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                    fail_silently=False,
                )
                return redirect('reservations:make_reservation')
    else:
        form = ReservationForm()
    return render(request, 'reservations/make_reservation.html', {'form': form})
