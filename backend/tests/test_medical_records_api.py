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
class TestMedicalRecordsAPI:
    def setup_method(self):
        self.client = APIClient()
        self.specialty = Specialty.objects.create(name='Tai Mũi Họng', code='CK-TMH')
        self.doc_user = User.objects.create_user(username='doctor_test', password='DocPassword@123', role='DOCTOR')
        self.doctor = Doctor.objects.create(user=self.doc_user, code='BS-TMH01', specialty=self.specialty, room_number='201', phone='0988111333')
        self.patient = Patient.objects.create(code='BN-TMH01', full_name='Trần Bệnh Nhân', date_of_birth='1992-05-10', gender='FEMALE', phone='0977111222', address='Hà Nội')

        self.appointment = Appointment.objects.create(
            code='LH-MED-01',
            patient=self.patient,
            doctor=self.doctor,
            specialty=self.specialty,
            appointment_date=timezone.localdate(),
            start_time=time(8, 0),
            end_time=time(8, 30),
            status='IN_PROGRESS',
            reason='Viêm họng hạt'
        )

    def test_doctor_can_create_medical_record(self):
        self.client.force_authenticate(user=self.doc_user)
        data = {
            'appointment': self.appointment.id,
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'symptoms': 'Ho đờm, đau rát cổ họng 3 ngày',
            'vital_signs': {'temp': '37.5 C', 'bp': '120/80'},
            'diagnosis': 'Viêm họng cấp tính',
            'treatment_plan': 'Súc họng nước muối, uống kháng sinh theo đơn',
            'prescription': [{'medicine': 'Augmentin 1g', 'quantity': '14 viên', 'dosage': '2v/ngày'}]
        }
        response = self.client.post('/api/medical-records/', data, format='json')
        assert response.status_code == 201
        assert response.data['code'].startswith('BA-')

        # Xác nhận trạng thái lịch hẹn chuyển sang COMPLETED
        self.appointment.refresh_from_db()
        assert self.appointment.status == 'COMPLETED'

    def test_receptionist_cannot_create_medical_record(self):
        rec_user = User.objects.create_user(username='rec_unauthorized', password='Pass@123', role='RECEPTIONIST')
        self.client.force_authenticate(user=rec_user)
        data = {
            'appointment': self.appointment.id,
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'symptoms': 'Sốt',
            'diagnosis': 'Cảm cúm',
            'treatment_plan': 'Nghỉ ngơi'
        }
        response = self.client.post('/api/medical-records/', data, format='json')
        assert response.status_code == 403
