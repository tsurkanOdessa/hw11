from django.urls import path
from .views import (
    APITaskCreateView,
    APITaskListView,
    APITaskDetailView,
    APITaskStatsView,
    task_list_view
)
urlpatterns = [
    #Templates
    path('', task_list_view, name='task_list'),

    #API
    path('api/tasks/create/', APITaskCreateView.as_view(), name='api_task-create'),
    path('api/tasks/', APITaskListView.as_view(), name='api_task-list'),
    path('api/tasks/<int:id>/', APITaskDetailView.as_view(), name='api_task-detail'),
    path('api/tasks/stats/', APITaskStatsView.as_view(), name='api_task-stats'),
]
