from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'venue', 'category', 'organizer',
                  'capacity', 'available_seats', 'image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'organizer']

    def validate(self, attrs):
        if attrs.get('available_seats', 0) > attrs.get('capacity', 0):
            raise serializers.ValidationError("Available seats cannot exceed capacity.")
        return attrs