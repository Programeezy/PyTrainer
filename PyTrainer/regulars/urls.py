from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('task', views.get_task, name='index')
]
