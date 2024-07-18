from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reserve/<int:spot_id>/', views.create_reservation, name='create_reservation'),
    path('parking-spots/', views.parking_spots_view, name='parking_spots'),
    path('reserve-spot/<int:spot_id>/', views.reserve_spot_view, name='reserve_spot'),
    path('reservation-success/', views.reservation_success_view, name='reservation_success'),
    path('mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),
    path('verify-and-reserve/', views.verify_and_reserve, name='verify_and_reserve'),
    path('calculate-payment-amount/', views.calculate_payment_amount, name='calculate_payment_amount'),
    path('check-availability/', views.check_availability, name='check_availability'),
    path('about/', views.about, name='about'),
]
