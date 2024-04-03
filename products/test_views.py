from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import NewUser, Product
from products.serializers import NewUserDetailSerializer, ProductSerializer
from products.views import LoginViewSet, ProductsViewSet
from django.test import TestCase
from rest_framework.test import APIClient


class LoginViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = NewUser.objects.create(email="test@example.com", username="testuser")
        self.user.set_password("testpassword")
        self.user.save()

    def test_login_success(self):
        data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post('/login/', data)
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_credentials(self):
        data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        response = self.client.post('/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_credentials(self):
        data = {}
        response = self.client.post('/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductsViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = NewUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.superuser = NewUser.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword')
        self.client.login(username='admin', password='adminpassword')
        self.product = Product.objects.create(title='Test Product', price=10.00, owner=self.user)

    def test_list_products(self):
        url = reverse('products-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_authenticated_superuser(self):
        url = reverse('products-list')
        data = {'title': 'New Product', 'price': 15.00, 'description': 'New Product', 'category': 'New Product', 'image': 'New Product'}
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_unauthenticated(self):
        url = reverse('products-list')
        data = {'title': 'New Product', 'price': 15.00, 'description': 'New Product', 'category': 'New Product', 'image': 'New Product'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_owner(self):
        url = reverse('products-detail', kwargs={'pk': self.product.pk})
        data = {'title': 'Updated Product', 'price': 15.00, 'description': 'New Product', 'category': 'New Product', 'image': 'New Product'}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductsViewSetTestCaseNotOwner(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = NewUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.superuser = NewUser.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword')
        self.product = Product.objects.create(title='Test Product', price=10.00, owner=self.user)

    def test_update_product_not_owner(self):
        url = reverse('products-detail', kwargs={'pk': self.product.pk})
        data = {'title': 'Updated Product', 'price': 15.00, 'description': 'New Product', 'category': 'New Product', 'image': 'New Product'}
        self.client.force_authenticate(user=self.superuser)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)