from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAttendee
from .models import Registration
from .serializers import RegistrationSerializer


class RegistrationListCreateView(generics.ListCreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Registration.objects.all()
        elif self.request.user.role == 'organizer':
            return Registration.objects.filter(event__organizer=self.request.user)
        return Registration.objects.filter(attendee=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.role != 'attendee':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only attendees can register for events.")
        serializer.save(attendee=self.request.user)


class RegistrationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Registration.objects.all()
        elif self.request.user.role == 'organizer':
            return Registration.objects.filter(event__organizer=self.request.user)
        return Registration.objects.filter(attendee=self.request.user)
