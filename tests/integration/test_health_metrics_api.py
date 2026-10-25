import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestObservabilityAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_health_endpoint(self):
        response = self.client.get('/api/health/')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        assert data['database'] == 'healthy'
        assert data['service'] == 'clinic-backend'

    def test_metrics_endpoint(self):
        response = self.client.get('/api/metrics/')
        assert response.status_code == 200
        assert 'python_info' in response.content.decode() or 'django_' in response.content.decode() or 'process_' in response.content.decode()
