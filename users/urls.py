from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register', views.register,name='register'),
    path('register_handle', views.register_handle, name='register_handle'),
    path('login', views.login, name='login'),
    path('login_check', views.login_check, name='login_check'),
    path('logout', views.logout, name='logout'),
    path('', views.user, name='user'),
    ]
