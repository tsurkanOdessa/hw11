from django.urls import path
from .views import (
# Template
    task_list_view,
#API Task
    APITaskCreateView,
    APITaskListView,
    APITaskDetailView,
    APITaskStatsView,
    APITaskByWeekdayView,
#API Category
    APICategoryListCreateView,
    APICategoryRetrieveUpdateDestroyView,
#API SubTask
    APISubTaskListCreateView,
    APISubTaskDetailUpdateDeleteView

)



urlpatterns = [
    # Templates
    path('', task_list_view, name='task_list'),

    # API
    path('api/tasks/create/', APITaskCreateView.as_view(), name='api_task-create'),
    path('api/tasks/', APITaskListView.as_view(), name='api_task-list'),
    path('api/tasks/<int:id>/', APITaskDetailView.as_view(), name='api_task-detail'),
    path('api/tasks/stats/', APITaskStatsView.as_view(), name='api_task-stats'),
    path('api/tasks/by-weekday/<str:weekday>/', APITaskByWeekdayView.as_view(), name='tasks-by-weekday'),

    path('api/categories/', APICategoryListCreateView.as_view(), name='category-list-create'),
    path('api/categories/<int:pk>/', APICategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),

    path('api/subtasks/', APISubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('api/subtasks/<int:pk>/', APISubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail'),


]