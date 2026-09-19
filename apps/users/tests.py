from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.statuses.models import Status
from apps.tasks.models import Task


class UserCrudTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='ivan',
            password='Secret123!',
            first_name='Иван',
            last_name='Петров',
        )

    def test_user_list_available_without_login(self):
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ivan')

    def test_user_create(self):
        response = self.client.post(reverse('users:create'), {
            'first_name': 'Пётр',
            'last_name': 'Сидоров',
            'username': 'petr',
            'password1': 'Secret123!',
            'password2': 'Secret123!',
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='petr').exists())

    def test_user_create_duplicate_username(self):
        response = self.client.post(reverse('users:create'), {
            'first_name': 'Пётр',
            'last_name': 'Сидоров',
            'username': 'ivan',
            'password1': 'Secret123!',
            'password2': 'Secret123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'уже существует')

    def test_user_update_by_self(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('users:update', args=[self.user.id]), {
            'first_name': 'Иван',
            'last_name': 'Петров',
            'username': 'ivan_new',
        })
        self.assertRedirects(response, reverse('users:list'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'ivan_new')

    def test_user_cannot_update_other(self):
        other = User.objects.create_user(username='petr', password='Secret123!')
        self.client.force_login(self.user)
        response = self.client.get(reverse('users:update', args=[other.id]))
        self.assertRedirects(response, reverse('users:list'))

    def test_user_delete_by_self(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('users:delete', args=[self.user.id]))
        self.assertRedirects(response, reverse('users:list'))
        self.assertFalse(User.objects.filter(username='ivan').exists())

    def test_user_cannot_delete_other(self):
        other = User.objects.create_user(username='petr', password='Secret123!')
        self.client.force_login(self.user)
        response = self.client.get(reverse('users:delete', args=[other.id]))
        self.assertRedirects(response, reverse('users:list'))
        self.assertTrue(User.objects.filter(username='petr').exists())

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'ivan',
            'password': 'Secret123!',
        })
        self.assertRedirects(response, reverse('index'))

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('index'))


class UserProtectedFromDeletionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='Secret123!')
        self.status = Status.objects.create(name='Новый')
        self.task = Task.objects.create(
            name='Test task',
            status=self.status,
            author=self.user,
        )

    def test_cannot_delete_user_author_of_task(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('users:delete', args=[self.user.id]))
        self.assertRedirects(response, reverse('users:list'))
        self.assertTrue(User.objects.filter(username='ivan').exists())