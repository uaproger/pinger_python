from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Service


class ServiceApiTests(APITestCase):
    def setUp(self):
        """Налаштування перед кожним тестом"""
        # Створюємо тестового користувача (Виконання Пункту 8)
        self.user = User.objects.create_user(username='testuser', password='password123')
        # Виконуємо примусову авторизацію для всіх запитів (Виконання Пункту 8)
        self.client.force_authenticate(user=self.user)
        self.service_data = {'name': 'Google', 'url': 'https://google.com'}

    def test_service_model_logic(self):
        """Тест базової логіки створення моделі"""
        service = Service.objects.create(name="Manual", url="https://manual.com", owner=self.user)
        self.assertEqual(service.name, "Manual")
        self.assertEqual(service.owner.username, 'testuser')

    def test_api_list_access(self):
        """Тест доступу до списку сервісів через REST API"""
        url = reverse('service-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_service_via_rest_api(self):
        """Тест створення об'єкта через REST API"""
        url = reverse('service-list')
        response = self.client.post(url, self.service_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Service.objects.filter(owner=self.user).count(), 1)

    def test_data_isolation_between_users(self):
        """Тест пермішинів та ізоляції даних"""
        # Створюємо сервіс для поточного юзера
        Service.objects.create(name="User Own Service", url="https://own.com", owner=self.user)

        # Створюємо іншого юзера та його сервіс
        other_user = User.objects.create_user(username='stranger', password='password')
        Service.objects.create(name="Stranger Service", url="https://stranger.com", owner=other_user)

        response = self.client.get(reverse('service-list'))
        # Очікуємо лише 1 запис, що належить поточному юзеру
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "User Own Service")
