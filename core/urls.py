from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.signin, name='login'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('theme/', views.theme, name='theme'),
]
