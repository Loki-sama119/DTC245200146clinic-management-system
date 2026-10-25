import pytest
from datetime import time, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.specialties.models import Specialty
from apps.appointments.models import Appointment

User = get_user_model()

@pytest.mark.django_db
class TestAppointmentsAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='receptionist_test', password='Pass@123', role='RECEPTIONIST')
        self.client.force_authenticate(user=self.user)

        self.specialty = Specialty.objects.create(name='Nội Khoa Test', code='CK-TEST')
        doc_user = User.objects.create_user(username='doc_test', password='Pass@123', role='DOCTOR')
        self.doctor = Doctor.objects.create(
            user=doc_user,
            code='BS-TEST',
            specialty=self.specialty,
            room_number='101',
            phone='0988111222'
        )
        self.patient = Patient.objects.create(
            code='BN-TEST01',
            full_name='Bệnh Nhân Test',
            date_of_birth='1990-01-01',
            gender='MALE',
            phone='0911222333',
            address='Hà Nội'
        )

    def test_create_appointment_success(self):
        today = timezone.localdate() + timedelta(days=1)
        data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'specialty': self.specialty.id,
            'appointment_date': str(today),
            'start_time': '09:00:00',
            'end_time': '09:30:00',
            'reason': 'Khám định kỳ'
        }
        response = self.client.post('/api/appointments/', data)
        assert response.status_code == 201
        assert response.data['code'].startswith('LH-')
        assert response.data['status'] == 'PENDING'

    def test_anti_conflict_overlap_detection(self):
        today = timezone.localdate() + timedelta(days=1)
        # Tạo lịch 1: 09:00 - 09:30
        Appointment.objects.create(
            code='LH-CONFLICT-1',
            patient=self.patient,
            doctor=self.doctor,
            specialty=self.specialty,
            appointment_date=today,
            start_time=time(9, 0),
            end_time=time(9, 30),
            status='CONFIRMED',
            reason='Khám 1'
        )

        # Thử đặt lịch 2 trùng khung giờ (09:15 - 09:45) cho cùng bác sĩ
        data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'specialty': self.specialty.id,
            'appointment_date': str(today),
            'start_time': '09:15:00',
            'end_time': '09:45:00',
            'reason': 'Khám trùng giờ'
        }
        response = self.client.post('/api/appointments/', data)
        assert response.status_code == 400
        assert 'start_time' in response.data

    def test_past_date_appointment_rejected(self):
        yesterday = timezone.localdate() - timedelta(days=1)
        data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'specialty': self.specialty.id,
            'appointment_date': str(yesterday),
            'start_time': '09:00:00',
            'end_time': '09:30:00',
            'reason': 'Khám quá khứ'
        }
        response = self.client.post('/api/appointments/', data)
        assert response.status_code == 400

    def test_appointment_status_transitions(self):
        today = timezone.localdate() + timedelta(days=1)
        apt = Appointment.objects.create(
            code='LH-TRANS-1',
            patient=self.patient,
            doctor=self.doctor,
            specialty=self.specialty,
            appointment_date=today,
            start_time=time(10, 0),
            end_time=time(10, 30),
            status='PENDING',
            reason='Test chuyển trạng thái'
        )

        # 1. Confirm
        res = self.client.post(f'/api/appointments/{apt.id}/confirm/')
        assert res.status_code == 200
        apt.refresh_from_db()
        assert apt.status == 'CONFIRMED'

        # 2. Check-in
        res = self.client.post(f'/api/appointments/{apt.id}/check-in/')
        assert res.status_code == 200
        apt.refresh_from_db()
        assert apt.status == 'IN_PROGRESS'

        # 3. Complete
        res = self.client.post(f'/api/appointments/{apt.id}/complete/')
        assert res.status_code == 200
        apt.refresh_from_db()
        assert apt.status == 'COMPLETED'
