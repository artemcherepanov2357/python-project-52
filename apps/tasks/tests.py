from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.labels.models import Label
from apps.statuses.models import Status

from .models import Task


class TaskCrudTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='Secret123!')
        self.other = User.objects.create_user(username='petr', password='Secret123!')
        self.status = Status.objects.create(name='Новый')
        self.label = Label.objects.create(name='Important')
        self.client.force_login(self.user)

    def test_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('tasks:list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_list_ok(self):
        Task.objects.create(name='Test', status=self.status, author=self.user)
        response = self.client.get(reverse('tasks:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_create(self):
        response = self.client.post(reverse('tasks:create'), {
            'name': 'New task',
            'description': 'Description',
            'status': self.status.id,
            'executor': self.other.id,
            'labels': [self.label.id],
        })
        self.assertRedirects(response, reverse('tasks:list'))
        task = Task.objects.get(name='New task')
        self.assertEqual(task.author, self.user)
        self.assertEqual(task.executor, self.other)

    def test_create_duplicate_name(self):
        Task.objects.create(name='Test', status=self.status, author=self.user)
        response = self.client.post(reverse('tasks:create'), {
            'name': 'Test',
            'description': '',
            'status': self.status.id,
            'executor': '',
            'labels': [],
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'уже существует')

    def test_detail(self):
        task = Task.objects.create(name='Test', status=self.status, author=self.user)
        response = self.client.get(reverse('tasks:detail', args=[task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_update(self):
        task = Task.objects.create(name='Old', status=self.status, author=self.user)
        response = self.client.post(reverse('tasks:update', args=[task.id]), {
            'name': 'Updated',
            'description': 'New desc',
            'status': self.status.id,
            'executor': '',
            'labels': [],
        })
        self.assertRedirects(response, reverse('tasks:list'))
        task.refresh_from_db()
        self.assertEqual(task.name, 'Updated')

    def test_delete_by_author(self):
        task = Task.objects.create(name='Test', status=self.status, author=self.user)
        response = self.client.post(reverse('tasks:delete', args=[task.id]))
        self.assertRedirects(response, reverse('tasks:list'))
        self.assertFalse(Task.objects.filter(name='Test').exists())

    def test_cannot_delete_by_other(self):
        task = Task.objects.create(name='Test', status=self.status, author=self.user)
        self.client.force_login(self.other)
        response = self.client.post(reverse('tasks:delete', args=[task.id]))
        self.assertRedirects(response, reverse('tasks:list'))
        self.assertTrue(Task.objects.filter(name='Test').exists())

class TaskFilterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='Secret123!')
        self.other = User.objects.create_user(username='petr', password='Secret123!')
        self.status_new = Status.objects.create(name='Новый')
        self.status_done = Status.objects.create(name='Завершён')
        self.label = Label.objects.create(name='Important')
        self.client.force_login(self.user)

        self.t1 = Task.objects.create(name='Mine new', status=self.status_new, author=self.user)
        self.t2 = Task.objects.create(name='Other done', status=self.status_done, author=self.other)
        self.t3 = Task.objects.create(name='With label', status=self.status_new, author=self.other)
        self.t3.labels.add(self.label)

    def test_filter_by_status(self):
        response = self.client.get(reverse('tasks:list'), {'status': self.status_new.id})
        self.assertContains(response, 'Mine new')
        self.assertContains(response, 'With label')
        self.assertNotContains(response, 'Other done')

    def test_filter_by_executor(self):
        self.t2.executor = self.user
        self.t2.save()
        response = self.client.get(reverse('tasks:list'), {'executor': self.user.id})
        self.assertContains(response, 'Other done')
        self.assertNotContains(response, 'Mine new')

    def test_filter_by_label(self):
        response = self.client.get(reverse('tasks:list'), {'labels': self.label.id})
        self.assertContains(response, 'With label')
        self.assertNotContains(response, 'Mine new')

    def test_filter_self_tasks(self):
        response = self.client.get(reverse('tasks:list'), {'self_tasks': 'on'})
        self.assertContains(response, 'Mine new')
        self.assertNotContains(response, 'Other done')
        self.assertNotContains(response, 'With label')