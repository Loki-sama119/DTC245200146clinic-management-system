import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.mark.django_db
class TestAuthAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test_user',
            password='TestPassword@123',
            role='RECEPTIONIST',
            email='test@clinic.vn'
        )

    def test_login_success(self):
        response = self.client.post('/api/auth/login/', {
            'username': 'test_user',
            'password': 'TestPassword@123'
        })
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['username'] == 'test_user'

    def test_login_wrong_password(self):
        response = self.client.post('/api/auth/login/', {
            'username': 'test_user',
            'password': 'WrongPassword'
        })
        assert response.status_code == 401

    def test_me_endpoint_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/auth/me/')
        assert response.status_code == 200
        assert response.data['username'] == 'test_user'

    def test_me_endpoint_unauthenticated(self):
        response = self.client.get('/api/auth/me/')
        assert response.status_code == 401
