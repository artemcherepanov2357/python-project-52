from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=200, unique=True)     # ← unique=True
    description = models.TextField(blank=True)
    status = models.ForeignKey(
        'statuses.Status',
        on_delete=models.PROTECT,
        related_name='tasks',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='authored_tasks',
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='assigned_tasks',
    )
    labels = models.ManyToManyField(
        'labels.Label',
        blank=True,
        related_name='tasks',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name