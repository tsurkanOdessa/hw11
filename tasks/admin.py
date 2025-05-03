from django.contrib import admin
from .models import Task, SubTask

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]
    list_display = ['short_title']

    def short_title(self, obj):
        return obj.title if len(obj.title) <= 10 else obj.title[:10] + '...'
    short_title.short_description = "Название"
