from django.test import TestCase
from .models import Service


class ServiceModelTest(TestCase):
    def test_service_creation(self):
        service = Service.objects.create(name="Google", url="https://google.com")
        self.assertEqual(service.name, "Google")

    def test_api_status(self):
        response = self.client.get('/api/services/')
        self.assertEqual(response.status_code, 200)
