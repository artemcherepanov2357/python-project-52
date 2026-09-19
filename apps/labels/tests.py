from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.statuses.models import Status
from apps.tasks.models import Task

from .models import Label


class LabelCrudTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='Secret123!')
        self.client.force_login(self.user)

    def test_create(self):
        response = self.client.post(reverse('labels:create'), {'name': 'Important'})
        self.assertRedirects(response, reverse('labels:list'))
        self.assertTrue(Label.objects.filter(name='Important').exists())

    def test_update(self):
        label = Label.objects.create(name='Old')
        response = self.client.post(reverse('labels:update', args=[label.id]), {'name': 'New'})
        self.assertRedirects(response, reverse('labels:list'))
        label.refresh_from_db()
        self.assertEqual(label.name, 'New')

    def test_delete(self):
        label = Label.objects.create(name='Temp')
        response = self.client.post(reverse('labels:delete', args=[label.id]))
        self.assertRedirects(response, reverse('labels:list'))
        self.assertFalse(Label.objects.filter(name='Temp').exists())

    def test_cannot_delete_label_with_tasks(self):
        label = Label.objects.create(name='Important')
        status = Status.objects.create(name='Новый')
        task = Task.objects.create(name='Test', status=status, author=self.user)
        task.labels.add(label)
        response = self.client.post(reverse('labels:delete', args=[label.id]))
        self.assertRedirects(response, reverse('labels:list'))
        self.assertTrue(Label.objects.filter(name='Important').exists())