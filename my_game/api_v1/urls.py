from django.urls import path

from .views import (
    my_tasks_list_view,
    my_tasks_detail_view,
)


app_name = 'game'

urlpatterns = [
    path(r'my-tasks/', my_tasks_list_view, name='task-list'),
    path(r'my-tasks/<int:task_type>/', my_tasks_detail_view, name='task-detail'),
]