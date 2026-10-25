import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.patients.models import Patient

User = get_user_model()

@pytest.mark.django_db
class TestPatientsAPI:
    def setup_method(self):
        self.client = APIClient()
        self.receptionist = User.objects.create_user(
            username='rec_staff',
            password='StaffPassword@123',
            role='RECEPTIONIST'
        )
        self.client.force_authenticate(user=self.receptionist)

    def test_create_patient(self):
        data = {
            'full_name': 'Nguyễn Văn Test',
            'date_of_birth': '1995-01-01',
            'gender': 'MALE',
            'phone': '0988000111',
            'address': 'Hà Nội',
            'blood_type': 'O+'
        }
        response = self.client.post('/api/patients/', data)
        assert response.status_code == 201
        assert response.data['full_name'] == 'Nguyễn Văn Test'
        assert response.data['code'].startswith('BN-')

    def test_duplicate_phone_rejected(self):
        Patient.objects.create(
            code='BN-11111',
            full_name='BN Gốc',
            date_of_birth='1990-01-01',
            gender='FEMALE',
            phone='0988000222',
            address='Hà Nội'
        )
        data = {
            'full_name': 'BN Trùng SĐT',
            'date_of_birth': '1992-02-02',
            'gender': 'MALE',
            'phone': '0988000222',
            'address': 'Hà Nội'
        }
        response = self.client.post('/api/patients/', data)
        assert response.status_code == 400

    def test_search_patient(self):
        Patient.objects.create(
            code='BN-99991',
            full_name='Hoàng Minh Thông',
            date_of_birth='1988-05-10',
            gender='MALE',
            phone='0977889900',
            address='Đà Nẵng'
        )
        response = self.client.get('/api/patients/?search=Hoàng Minh Thông')
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['code'] == 'BN-99991'
