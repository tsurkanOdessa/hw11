from django.db import models
from django.utils import timezone

STATUS_CHOICES = [
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
]

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def short_title(self):
        return self.title[:10]

    short_title.short_description = 'Short description'

    @property
    def is_overdue(self):
        if self.deadline:
            return timezone.now() > self.deadline
        return False