from django.contrib import admin
from .models import Venue


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'capacity', 'created_at', 'updated_at']
    search_fields = ['name', 'city', 'address']
    list_filter = ['city']
    ordering = ['name']
