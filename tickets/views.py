from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsOrganizerOrReadOnly, IsOrganizerOwnerOrAdmin
from .models import Ticket
from .serializers import TicketSerializer


class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsOrganizerOrReadOnly]


class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsOrganizerOwnerOrAdmin]
