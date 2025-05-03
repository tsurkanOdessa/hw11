from django.http import Http404
from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from django.utils import timezone
from django.shortcuts import render

from .models import Task, Category
from .serializers.tasks_serializer import TaskSerializer
from .serializers.category_serializer import CategoryCreateSerializer, CategorySerializer
from .models import SubTask
from .serializers.subtasks_serializer import SubTaskCreateSerializer


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


# Models View
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryCreateSerializer
        return CategorySerializer

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer


class SubTaskListCreateView(APIView):
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

class SubTaskDetailUpdateDeleteView(APIView):
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

class TaskByWeekdayListView(ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = SubTask.objects.select_related('task').all().order_by('-created_at')
        task_title = self.request.query_params.get('task_title')
        is_done = self.request.query_params.get('is_done')

        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)

        if is_done is not None:
            if is_done.lower() in ['true', '1']:
                queryset = queryset.filter(is_done=True)
            elif is_done.lower() in ['false', '0']:
                queryset = queryset.filter(is_done=False)

        return queryset

class SubTaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

class SubTaskListView(generics.ListAPIView):
    serializer_class = SubTaskCreateSerializer
    queryset = SubTask.objects.all().order_by('-created_at')
    pagination_class = SubTaskPagination


class FilteredSubTaskListView(generics.ListAPIView):
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination

    def get_queryset(self):
        queryset = SubTask.objects.select_related('task').all().order_by('-created_at')
        task_title = self.request.query_params.get('task_title')
        is_done = self.request.query_params.get('is_done')

        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)

        if is_done is not None:
            if is_done.lower() in ['true', '1']:
                queryset = queryset.filter(is_done=True)
            elif is_done.lower() in ['false', '0']:
                queryset = queryset.filter(is_done=False)

        return queryset
