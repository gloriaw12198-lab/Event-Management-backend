from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsOrganizerOrReadOnly
from .models import Venue
from .serializers import VenueSerializer


class VenueListCreateView(generics.ListCreateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsAuthenticated, IsOrganizerOrReadOnly]


class VenueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsAuthenticated, IsOrganizerOrReadOnly]
