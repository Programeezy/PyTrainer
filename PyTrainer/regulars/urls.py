from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('task', views.get_task, name='task'),
    path('history', views.show_history, name='history'),
    path('tasks', views.show_tasks, name='tasks')
]
