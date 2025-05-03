from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models.task import Task
from django.utils import timezone
from datetime import timedelta


class TaskAPITests(APITestCase):
    def setUp(self):

        self.task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'new',
            'deadline': (timezone.now() + timedelta(days=7)).isoformat()
        }


        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='in_progress',
            deadline=timezone.now() + timedelta(days=1))

        self.list_url = reverse('api_task-list')
        self.detail_url = reverse('api_task-detail', kwargs={'id': self.task.id})
        self.create_url = reverse('api_task-create')
        self.stats_url = reverse('api_task-stats')

    def test_create_task(self):
        response = self.client.post(self.create_url, self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.get(id=response.data['id']).title, 'Test Task')

    def test_get_task_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task')

    def test_get_task_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_task_stats(self):

        Task.objects.create(title='Task 2', status='new')
        Task.objects.create(title='Task 3', status='completed')

        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_tasks'], 3)
        self.assertEqual(
            next(item for item in response.data['status_stats'] if item['status'] == 'new')['count'],
            2
        )

    def test_invalid_deadline(self):
        invalid_data = self.task_data.copy()
        invalid_data['deadline'] = (timezone.now() - timedelta(days=1)).isoformat()

        response = self.client.post(self.create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('deadline', response.data)

    def test_update_task(self):
        updated_data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'status': 'completed'
        }

        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.status, 'completed')

    def test_delete_task(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)