
from rest_framework.test import APITestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task, SubTask
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


class TaskByWeekdayTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.task_mon = Task.objects.create(
            title='Task Monday',
            created_at=timezone.now() - timedelta(days=timezone.now().weekday()),  # Monday
        )
        self.task_fri = Task.objects.create(
            title='Task Friday',
            created_at=timezone.now() - timedelta(days=timezone.now().weekday() - 4),  # Friday
        )

    def test_no_weekday_param_returns_all(self):
        response = self.client.get('/api/tasks/by-weekday/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_monday(self):
        response = self.client.get('/api/tasks/by-weekday/?weekday=Monday')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any('Monday' in task['title'] for task in response.data))

    def test_invalid_day_returns_empty(self):
        response = self.client.get('/api/tasks/by-weekday/?weekday=Notaday')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class SubTaskPaginationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        task = Task.objects.create(title='Main Task')
        for i in range(10):
            SubTask.objects.create(task=task, title=f'Subtask {i}', created_at=timezone.now() + timedelta(minutes=i))

    def test_subtask_pagination(self):
        response = self.client.get('/api/subtasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)  # Page size
        # Проверка сортировки по убыванию
        self.assertTrue(response.data['results'][0]['created_at'] > response.data['results'][1]['created_at'])


class FilteredSubTaskTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        task1 = Task.objects.create(title='Report')
        task2 = Task.objects.create(title='Meeting')

        SubTask.objects.create(task=task1, title='Write', is_done=False)
        SubTask.objects.create(task=task1, title='Edit', is_done=True)
        SubTask.objects.create(task=task2, title='Call', is_done=True)

    def test_filter_by_task_title(self):
        response = self.client.get('/api/subtasks/filtered/?task_title=Report')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all('Report' in sub['task'] for sub in response.data['results']))

    def test_filter_by_is_done(self):
        response = self.client.get('/api/subtasks/filtered/?is_done=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(sub['is_done'] is True for sub in response.data['results']))

    def test_filter_by_both(self):
        response = self.client.get('/api/subtasks/filtered/?task_title=Report&is_done=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
