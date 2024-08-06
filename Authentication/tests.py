from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model



User = get_user_model()

class TestAuthView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
    
    def test_signup_user(self):
        url = reverse('signup')
        data = {
            'username': 'johnDoe',
            'email': 'john.doe@gmail.com',
            'password': 'random_teStP@ssworD'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['username'], data['username'])
        self.assertEqual(response.data['data']['email'], data['email'])
    
    
    def test_signup_user_without_data(self):
        url = reverse('signup')
        data = {}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        username_error_message = str(response.data['data']['username'][0])
    
        self.assertEqual(username_error_message, 'This field is required.')
        
        password_error_message = str(response.data['data']['password'][0])
    
        self.assertEqual(password_error_message, 'This field is required.')
        
    
    def test_login_with_invalid_cred(self):
        url = reverse('login')
        data = {
            'username': 'random',
            'password': 'userPassW0rD'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_message = str(response.data['data']['non_field_errors'][0])
    
        self.assertEqual(error_message, 'Invalid login credentials.')
    
    def test_login_succeeds(self):
        url = reverse('login')
        data = {
            'username': self.user.username,
            'password': 'testpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data['data'])
        
    
    