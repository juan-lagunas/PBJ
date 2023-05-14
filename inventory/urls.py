from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.new, name='create'),
    path('add', views.add, name='add'),
    path('logs', views.logs, name='logs')
]