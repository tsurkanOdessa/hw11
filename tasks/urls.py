from django.urls import path
from .views import (
    APITaskCreateView,
    APITaskListView,
    APITaskDetailView,
    APITaskStatsView,
    task_list_view,
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView
)
urlpatterns = [
    #Templates
    path('', task_list_view, name='task_list'),

    #API
    path('api/tasks/create/', APITaskCreateView.as_view(), name='api_task-create'),
    path('api/tasks/', APITaskListView.as_view(), name='api_task-list'),
    path('api/tasks/<int:id>/', APITaskDetailView.as_view(), name='api_task-detail'),
    path('api/tasks/stats/', APITaskStatsView.as_view(), name='api_task-stats'),
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('api/categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    path('api/subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('api/subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
]
