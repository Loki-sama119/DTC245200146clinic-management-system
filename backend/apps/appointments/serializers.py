from rest_framework import serializers
from django.utils import timezone
from .models import Appointment
from apps.patients.serializers import PatientSerializer
from apps.doctors.serializers import DoctorSerializer
from apps.specialties.serializers import SpecialtySerializer
import random
from datetime import datetime, timedelta

class AppointmentSerializer(serializers.ModelSerializer):
    patient_details = PatientSerializer(source='patient', read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    specialty_name = serializers.CharField(source='specialty.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'code', 'patient', 'patient_details', 'doctor', 'doctor_details',
            'specialty', 'specialty_name', 'appointment_date', 'start_time', 'end_time',
            'status', 'reason', 'notes', 'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'code', 'created_at', 'updated_at']

    def validate(self, attrs):
        doctor = attrs.get('doctor') or (self.instance.doctor if self.instance else None)
        appointment_date = attrs.get('appointment_date') or (self.instance.appointment_date if self.instance else None)
        start_time = attrs.get('start_time') or (self.instance.start_time if self.instance else None)
        end_time = attrs.get('end_time') or (self.instance.end_time if self.instance else None)

        if not end_time and start_time:
            # Tự động tính end_time = start_time + 30 phút nếu không truyền
            dummy_date = datetime(2000, 1, 1, start_time.hour, start_time.minute, start_time.second)
            attrs['end_time'] = (dummy_date + timedelta(minutes=30)).time()
            end_time = attrs['end_time']

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError({"end_time": "Giờ kết thúc phải lớn hơn giờ bắt đầu."})

        # Kiểm tra không đặt lịch trong quá khứ đối với tạo mới
        if not self.instance and appointment_date and appointment_date < timezone.localdate():
            raise serializers.ValidationError({"appointment_date": "Không thể tạo lịch hẹn trong quá khứ."})

        # Kiểm tra bác sĩ có đang hoạt động hay không
        if doctor and not doctor.is_active:
            raise serializers.ValidationError({"doctor": "Bác sĩ này hiện đang tạm ngừng công tác, không thể nhận lịch hẹn mới."})

        # Thuật toán kiểm tra trùng lịch (Interval Overlap Prevention):
        # start_time < existing.end_time AND end_time > existing.start_time
        if doctor and appointment_date and start_time and end_time:
            conflict_query = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                status__in=[Appointment.Status.PENDING, Appointment.Status.CONFIRMED, Appointment.Status.IN_PROGRESS],
                start_time__lt=end_time,
                end_time__gt=start_time
            )

            if self.instance:
                conflict_query = conflict_query.exclude(id=self.instance.id)

            if conflict_query.exists():
                conflict_apt = conflict_query.first()
                raise serializers.ValidationError({
                    "start_time": f"Bác sĩ {doctor.code} đã có lịch khám khác trong khung giờ {conflict_apt.start_time.strftime('%H:%M')} - {conflict_apt.end_time.strftime('%H:%M')} ngày {appointment_date}. Vui lòng chọn khung giờ khác!"
                })

        return attrs

    def create(self, validated_data):
        if not validated_data.get('code'):
            for _ in range(10):
                code = f"LH-{random.randint(10000, 99999)}"
                if not Appointment.objects.filter(code=code).exists():
                    validated_data['code'] = code
                    break
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        return super().create(validated_data)
