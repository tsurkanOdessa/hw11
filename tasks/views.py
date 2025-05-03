from django.http import Http404
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from django.utils import timezone
from django.shortcuts import render

from .models import Task, Category, SubTask
from .serializers.tasks_serializer import TaskSerializer
from .serializers.category_serializer import CategoryCreateSerializer, CategorySerializer
from .serializers.subtasks_serializer import SubTaskCreateSerializer




WEEKDAY_MAPPING = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}

# Template View
def task_list_view(request):
    status_filter = request.GET.get('status', None)
    tasks = Task.objects.all()
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    context = {
        'tasks': tasks,
        'new_tasks_count': Task.objects.filter(status='new').count(),
        'in_progress_tasks_count': Task.objects.filter(status='in_progress').count(),
        'completed_tasks_count': Task.objects.filter(status='completed').count(),
    }

    return render(request, 'task_list.html', context)

# API Task Views
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

class APITaskByWeekdayView(APIView):
    def get(self, request, weekday, format=None):
        if weekday.isdigit():
            weekday_number = int(weekday) - 1
        else:
            weekday_number = WEEKDAY_MAPPING.get(weekday.lower())

        if weekday_number is None or weekday_number < 0 or weekday_number > 6:
            return Response({"error": "Неверное название или номер дня недели"}, status=status.HTTP_400_BAD_REQUEST)

        tasks = Task.objects.filter(
            deadline__week_day=weekday_number + 1)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# API Category Views
class APICategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryCreateSerializer
        return CategorySerializer

class APICategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

# API SubTask Views
class APISubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskCreateSerializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class APISubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

