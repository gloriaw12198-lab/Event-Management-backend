from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'venue', 'category', 'organizer', 'capacity', 'available_seats']
    search_fields = ['title', 'description']
    list_filter = ['date', 'category', 'venue', 'organizer']
    ordering = ['-date', '-time']
