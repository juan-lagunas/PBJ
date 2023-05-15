from django.urls import path

from . import views

app_name = 'parts'

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('edit', views.edit, name='edit')
]