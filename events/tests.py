from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Event
from categories.models import Category
from venues.models import Venue

User = get_user_model()


class EventTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='organizer', email='org@example.com', password='testpass123', role='organizer')
        self.category = Category.objects.create(name='Technology')
        self.venue = Venue.objects.create(name='Tech Hub', address='123 Tech St', city='Nairobi', capacity=100)
        
    def test_create_event(self):
        self.client.force_authenticate(user=self.user)
        event_data = {
            'title': 'Tech Conference',
            'description': 'A great tech event',
            'date': '2024-12-01',
            'time': '09:00:00',
            'venue': self.venue.id,
            'category': self.category.id,
            'capacity': 100,
            'available_seats': 100
        }
        response = self.client.post('/api/events/', event_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Event.objects.filter(title='Tech Conference').exists())