from rest_framework import serializers
from .models import ParkingSpot, Reservation

class ParkingSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = '__all__'

    
    def validate(self, attrs):
        # Add validation logic here if needed
        return attrs

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


