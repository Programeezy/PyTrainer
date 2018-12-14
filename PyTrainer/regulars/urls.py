from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('task', views.get_task, name='task'),
    path('history', views.show_history, name='history'),
    path('tasks', views.show_tasks, name='tasks'),
    path('articles', views.show_articles, name='articles'),
    path('actions', views.show_actions, name='actions'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
]
