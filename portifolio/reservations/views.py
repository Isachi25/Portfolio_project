# reservations/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ParkingSpot, Reservation, Profile, Transaction
from .forms import UserRegistrationForm, ReservationForm
from datetime import datetime
from django.core.exceptions import ValidationError
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'reservations/index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            phone_number = form.cleaned_data['phone_number']
            profile = Profile(user=user, phone_number=phone_number)
            profile.save()

            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'reservations/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'reservations/login.html', {'error': 'Invalid credentials'})
    return render(request, 'reservations/login.html')

@login_required
def dashboard(request):
    parking_spots = ParkingSpot.objects.all()
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservations/dashboard.html', {'parking_spots': parking_spots, 'reservations': reservations})

@login_required
def create_reservation(request, spot_id):
    spot = get_object_or_404(ParkingSpot, id=spot_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.parking_spot = spot
            reservation.calculate_payment_amount()
            reservation.save()
            return redirect('dashboard')
    else:
        form = ReservationForm()
    return render(request, 'reservations/create_reservation.html', {'form': form, 'spot': spot})



@login_required
def update_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            updated_reservation = form.save(commit=False)
            updated_reservation.user = request.user
            updated_reservation.calculate_payment_amount()
            try:
                updated_reservation.save()
                return redirect('dashboard')
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservations/update_reservation.html', {'form': form, 'reservation': reservation})

@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        return redirect('dashboard')
    return render(request, 'reservations/delete_reservation.html', {'reservation': reservation})


# In your view
def parking_spots_view(request):
    parking_spots = ParkingSpot.objects.all()
    parking_spots_by_location = {}
    for spot in parking_spots:
        location_name = spot.get_location_display()
        if location_name not in parking_spots_by_location:
            parking_spots_by_location[location_name] = []
        parking_spots_by_location[location_name].append(spot)
    
    return render(request, 'reservations/dashboard.html', {'parking_spots_by_location': parking_spots_by_location})

@login_required
def parking_spots_view(request):
    # Fetch all parking spots from the database
    parking_spots = ParkingSpot.objects.all()
    
    # Organize parking spots by location
    parking_spots_by_location = {}
    for spot in parking_spots:
        location_name = spot.get_location_display()
        if location_name not in parking_spots_by_location:
            parking_spots_by_location[location_name] = []
        parking_spots_by_location[location_name].append(spot)
    
    # Pass the organized parking spots to the template context
    context = {
        'parking_spots_by_location': parking_spots_by_location,
    }
    
    return render(request, 'reservations/parking_spots.html', context)

@login_required
def reserve_spot_view(request, spot_id):
    spot = get_object_or_404(ParkingSpot, id=spot_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)  # Don't save to the database yet
            reservation.user = request.user
            reservation.parking_spot = spot  # Set the parking spot
            reservation.save()  # Now save the reservation with all data
            return redirect('reservation_success')  # Redirect to a success page
    else:
        form = ReservationForm()
    
    context = {
        'form': form,
        'spot': spot,
    }
    
    return render(request, 'reservations/reserve_spot.html', context)

@login_required
def reservation_success_view(request):
    return render(request, 'reservations/reservation_success.html')

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        mpesa_data = json.loads(request.body.decode('utf-8'))
        transaction = mpesa_data.get('Body').get('stkCallback').get('CallbackMetadata').get('Item')
        
        transaction_code = next((item['Value'] for item in transaction if item['Name'] == 'MpesaReceiptNumber'), None)
        amount = next((item['Value'] for item in transaction if item['Name'] == 'Amount'), None)
        phone_number = next((item['Value'] for item in transaction if item['Name'] == 'PhoneNumber'), None)
        
        # Save transaction details to the database
        Transaction.objects.create(
            transaction_code=transaction_code,
            amount=amount,
            phone_number=phone_number
        )
        
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
    else:
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid Request Method"})