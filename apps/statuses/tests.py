from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.tasks.models import Task

from .models import Status


class StatusCrudTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='Secret123!')
        self.client.force_login(self.user)

    def test_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('statuses:list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_list_ok(self):
        Status.objects.create(name='Новый')
        response = self.client.get(reverse('statuses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Новый')

    def test_create(self):
        response = self.client.post(reverse('statuses:create'), {'name': 'В работе'})
        self.assertRedirects(response, reverse('statuses:list'))
        self.assertTrue(Status.objects.filter(name='В работе').exists())

    def test_create_duplicate(self):
        Status.objects.create(name='Новый')
        response = self.client.post(reverse('statuses:create'), {'name': 'Новый'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'уже существует')

    def test_update(self):
        status = Status.objects.create(name='Новый')
        response = self.client.post(
            reverse('statuses:update', args=[status.id]),
            {'name': 'Обновлён'},
        )
        self.assertRedirects(response, reverse('statuses:list'))
        status.refresh_from_db()
        self.assertEqual(status.name, 'Обновлён')

    def test_delete(self):
        status = Status.objects.create(name='Новый')
        response = self.client.post(reverse('statuses:delete', args=[status.id]))
        self.assertRedirects(response, reverse('statuses:list'))
        self.assertFalse(Status.objects.filter(name='Новый').exists())

    def test_cannot_delete_status_with_tasks(self):
        status = Status.objects.create(name='Новый')
        Task.objects.create(name='Test', status=status, author=self.user)
        response = self.client.post(reverse('statuses:delete', args=[status.id]))
        self.assertRedirects(response, reverse('statuses:list'))
        self.assertTrue(Status.objects.filter(name='Новый').exists())