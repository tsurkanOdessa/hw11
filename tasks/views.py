from django.shortcuts import render
from .models import Task

def task_list(request):
    tasks = Task.objects.prefetch_related('subtasks')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})
