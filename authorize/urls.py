from django.urls import path

from . import views

app_name = 'authorize'
urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('login_auth', views.login_auth, name='login_auth'),
    path('register', views.register, name='register'),
    path('register_auth', views.register_auth, name='register_auth'),
]