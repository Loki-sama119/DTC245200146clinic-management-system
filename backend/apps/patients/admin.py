from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('code', 'full_name', 'gender', 'phone', 'date_of_birth', 'is_active', 'created_at')
    list_filter = ('gender', 'is_active', 'blood_type')
    search_fields = ('code', 'full_name', 'phone', 'identity_number')
