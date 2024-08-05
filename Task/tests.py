from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Task


User = get_user_model()

class TaskAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status='pending',
            assigned_to=self.user,
            created_by=self.user,
            due_date='2024-08-03T12:00:00Z'
        )
    
    def test_create_task(self):
        url = reverse('tasks')
        data = {
            'name': 'New Task',
            'description': 'New Description',
            'status': 'pending',
            'due_date': '2024-08-03T12:00:00Z'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], 'New Task')
    
    def test_create_task_with_invalid_assigned_user_id(self):
        url = reverse('tasks')
        data = {
            'name': 'New Task',
            'description': 'New Description',
            'status': 'pending',
            'due_date': '2024-08-03T12:00:00Z',
            'assigned_to_id': '2'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['errors'], {'message': 'assigned to user does not exist'})
    
    def test_create_task_without_data(self):
        url = reverse('tasks')
        data = {}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['name'], ['This field is required.'])
        self.assertEqual(response.data['status'], ['This field is required.'])
        self.assertEqual(response.data['due_date'], ['This field is required.'])


    def test_list_tasks(self):
        url = reverse('tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['tasks']), 1)
        self.assertEqual(response.data['data']['tasks'][0]['name'], self.task.name)

    def test_list_tasks_filter_status(self):
        url = reverse('tasks')
        response = self.client.get(url, {'status': 'pending'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['tasks']), 1)
        for task in response.data['data']['tasks']:
            self.assertEqual(task['status'], 'pending')

    def test_list_tasks_filter_due_date(self):
        url = reverse('tasks')
        due_date = (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.get(url, {'due_date': due_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_list_tasks_filter_status_and_due_date(self):
        url = reverse('tasks')
        due_date = (timezone.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.get(url, {'status': 'completed', 'due_date': due_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_task(self):
        url = reverse('task_detail', args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], self.task.name)

    def test_update_task(self):
        url = reverse('task_detail', args=[self.task.id])
        data = {'name': 'Updated Task Name'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Updated Task Name')

    def test_delete_task(self):
        url = reverse('task_detail', args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
