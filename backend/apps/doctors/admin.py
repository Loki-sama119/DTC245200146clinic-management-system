from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'specialty', 'room_number', 'phone', 'is_active')
    list_filter = ('specialty', 'is_active')
    search_fields = ('code', 'user__first_name', 'user__last_name', 'phone')
