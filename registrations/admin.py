from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['attendee', 'event', 'ticket', 'status', 'registration_date']
    search_fields = ['attendee__username', 'event__title']
    list_filter = ['status', 'event', 'ticket']
    ordering = ['-registration_date']
