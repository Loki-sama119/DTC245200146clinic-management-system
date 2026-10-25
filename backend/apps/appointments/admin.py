from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'patient', 'doctor', 'specialty', 'appointment_date', 'start_time', 'status')
    list_filter = ('status', 'appointment_date', 'specialty')
    search_fields = ('code', 'patient__full_name', 'doctor__code')
