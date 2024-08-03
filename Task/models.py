from django.db import models
from django.contrib.auth import get_user_model

from uuid import uuid4


User = get_user_model()


class Task(models.Model):
    STATUS = (
        ("pending", "pending"),
        ("in_progress", "in_progress"),
        ("completed", "completed")
    )

    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField()
    status = models.CharField(choices=STATUS, max_length=50, default=STATUS[0][0])

    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_by")
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_to")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
