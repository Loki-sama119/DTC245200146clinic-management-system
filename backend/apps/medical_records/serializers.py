from rest_framework import serializers
from .models import MedicalRecord
from apps.patients.serializers import PatientSerializer
from apps.doctors.serializers import DoctorSerializer
import random

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_details = PatientSerializer(source='patient', read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    appointment_code = serializers.CharField(source='appointment.code', read_only=True)

    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'code', 'appointment', 'appointment_code', 'patient', 'patient_details',
            'doctor', 'doctor_details', 'symptoms', 'vital_signs', 'diagnosis',
            'treatment_plan', 'prescription', 'doctor_notes', 'follow_up_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'code', 'created_at', 'updated_at']

    def create(self, validated_data):
        if not validated_data.get('code'):
            for _ in range(10):
                code = f"BA-{random.randint(10000, 99999)}"
                if not MedicalRecord.objects.filter(code=code).exists():
                    validated_data['code'] = code
                    break

        # Tự động cập nhật trạng thái appointment sang COMPLETED
        record = super().create(validated_data)
        appointment = record.appointment
        appointment.status = 'COMPLETED'
        appointment.save()
        return record
