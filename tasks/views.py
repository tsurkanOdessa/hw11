from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q
from django.utils import timezone
from django.shortcuts import render

from .models import Task
from .serializers.tasks_serializer import TaskSerializer

# Template View
def task_list_view(request):
    tasks = Task.objects.all()

    context = {
        'tasks': tasks,
        'new_tasks_count': Task.objects.filter(status='new').count(),
        'in_progress_tasks_count': Task.objects.filter(status='in_progress').count(),
        'completed_tasks_count': Task.objects.filter(status='completed').count(),
    }

    return render(request, 'task_list.html', context)


# API View
class APITaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class APITaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class APITaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


class APITaskStatsView(APIView):
    def get(self, request):
        total_tasks = Task.objects.count()

        status_stats = Task.objects.values('status').annotate(
            count=Count('status')
        ).order_by('status')

        overdue_tasks = Task.objects.filter(
            deadline__lt=timezone.now()
        ).count()

        return Response({
            'total_tasks': total_tasks,
            'status_stats': status_stats,
            'overdue_tasks': overdue_tasks,
        })



