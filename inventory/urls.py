from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.index, name='index'),
    path('stock', views.stock, name='stock'),
    path('add', views.add, name='add'),
    path('logs', views.logs, name='logs'),
    path('checkout', views.checkout, name='checkout'),
    path('edit', views.edit, name='edit'),
    path('page', views.page, name='page')
]