from django.urls import path
from .views import home, register, login_view, dashboard, create_reservation, parking_spots_view, reserve_spot_view, reservation_success_view, mpesa_callback, verify_and_reserve, calculate_payment_amount, check_availability

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('reserve/<int:spot_id>/', create_reservation, name='create_reservation'),
    path('parking-spots/', parking_spots_view, name='parking_spots'),
    path('reserve-spot/<int:spot_id>/', reserve_spot_view, name='reserve_spot'),
    path('reservation-success/', reservation_success_view, name='reservation_success'),
    path('mpesa-callback/', mpesa_callback, name='mpesa_callback'),
    path('verify-and-reserve/', verify_and_reserve, name='verify_and_reserve'),
    path('calculate-payment-amount/', calculate_payment_amount, name='calculate_payment_amount'),
    path('check-availability/', check_availability, name='check_availability'),
    path('about/', views.about, name='about'),

]
