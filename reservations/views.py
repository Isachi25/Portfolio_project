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
from django.utils.dateparse import parse_datetime

def about(request):
    return render(request, 'about.html')

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
            return redirect('parking_spots')
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
            reservation = form.save(commit=False)
            reservation.parking_spot = spot
            reservation.user = request.user
            reservation.save()
            # Further processing if needed
    else:
        form = ReservationForm()
    return render(request, 'reservations/reserve_spot.html', {'form': form, 'spot': spot})

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


def verify_and_reserve(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        reservation_id = request.POST.get('reservation_id')

        try:
            reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            return JsonResponse({'error': 'Reservation not found.'}, status=404)

        # Verify the verification code (implement your verification logic here)
        if verification_code == reservation.transaction_code:
            reservation.payment_status = True
            reservation.save()
            return JsonResponse({'success': 'Reservation completed successfully.'})
        else:
            return JsonResponse({'error': 'Verification code incorrect.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def calculate_payment_amount(request):
    start_time = parse_datetime(request.GET.get('start_time'))
    end_time = parse_datetime(request.GET.get('end_time'))

    if start_time and end_time:
        duration = end_time - start_time
        total_minutes = duration.total_seconds() / 60
        if total_minutes <= 180:
            payment_amount = 150
        else:
            extra_minutes = total_minutes - 180
            payment_amount = 150 + extra_minutes

        return JsonResponse({'payment_amount': payment_amount})
    
    return JsonResponse({'error': 'Invalid date format'}, status=400)


@csrf_exempt
def check_availability(request):
    if request.method == 'GET':
        spot_id = request.GET.get('spot_id')
        start_time = parse_datetime(request.GET.get('start_time'))
        end_time = parse_datetime(request.GET.get('end_time'))
        
        overlapping_reservations = Reservation.objects.filter(
            parking_spot_id=spot_id,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if overlapping_reservations.exists():
            return JsonResponse({'available': False, 'message': 'The spot is not available at the selected time.'})
        else:
            return JsonResponse({'available': True})

    return JsonResponse({'available': False, 'message': 'Invalid request method.'})