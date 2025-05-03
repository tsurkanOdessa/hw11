from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def short_title(self):
        return self.title[:10]

    short_title.short_description = 'Short description'