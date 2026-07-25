from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['event', 'ticket_type', 'price', 'quantity', 'created_at', 'updated_at']
    search_fields = ['event__title', 'ticket_type']
    list_filter = ['ticket_type', 'event']
    ordering = ['event', 'ticket_type']
