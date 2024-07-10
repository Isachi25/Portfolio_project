from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import ParkingSpot, Reservation

class ParkingSpotTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.parking_spot_data = {'location': 'Test Location', 'spot_type': 'compact'}
    
    def test_create_parking_spot(self):
        url = '/api/parking_spots/'
        data = {'location': 'Test Location', 'spot_type': 'compact'}  # Example data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ReservationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.parking_spot = ParkingSpot.objects.create(location='Test Location', spot_type='compact')
        self.reservation_data = {
            'parking_spot': self.parking_spot.id,
            'start_time': '2023-06-30T10:00:00Z',
            'end_time': '2023-06-30T12:00:00Z',
            'user': 'testuser'
        }
    
    def test_create_reservation(self):
        response = self.client.post('/api/reservations/', self.reservation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.get().user, 'testuser')

#class PaymentTests(TestCase):

 #   def setUp(self):
  #      self.client = APIClient()
   #     self.reservation = Reservation.objects.create(
    #        parking_spot=ParkingSpot.objects.create(location='Test Location', spot_type='compact'),
     #       start_time='2023-06-30T10:00:00Z',
      #      end_time='2023-06-30T12:00:00Z',
       #     user='testuser'
        #)
        #self.payment_data = {
         #   'reservation': self.reservation.id,
          #  'amount': 20.00,
          #  'payment_method': 'credit card'
        #}
    
    #def test_create_payment(self):
     #   response = self.client.post('/api/payments/', self.payment_data, format='json')
      #  self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       # self.assertEqual(Payment.objects.count(), 1)
        #self.assertEqual(Payment.objects.get().amount, 20.00)


class OverlappingReservationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.parking_spot = ParkingSpot.objects.create(location='Test Location', spot_type='compact')
        self.reservation_data1 = {
            'parking_spot': self.parking_spot.id,
            'start_time': '2023-06-30T10:00:00Z',
            'end_time': '2023-06-30T12:00:00Z',
            'user': 'testuser1'
        }
        self.reservation_data2 = {
            'parking_spot': self.parking_spot.id,
            'start_time': '2023-06-30T11:00:00Z',
            'end_time': '2023-06-30T13:00:00Z',
            'user': 'testuser2'
        }
    
    def test_create_overlapping_reservation(self):
        response1 = self.client.post('/api/reservations/', self.reservation_data1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        response2 = self.client.post('/api/reservations/', self.reservation_data2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)