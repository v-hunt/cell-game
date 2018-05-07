from django.urls import path

from .views import (
    my_tasks_list_view,
    my_tasks_detail_view,
    game_field_view,
)


app_name = 'game'

urlpatterns = [
    path(r'my-tasks/', my_tasks_list_view, name='task-list'),
    path(r'my-tasks/<int:task_type>/', my_tasks_detail_view, name='task-detail'),
    path(r'field/', game_field_view, name='field'),

]