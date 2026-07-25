from rest_framework import serializers
from .models import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'attendee', 'event', 'ticket', 'status', 'registration_date', 'updated_at']
        read_only_fields = ['id', 'registration_date', 'updated_at', 'attendee']