from django.urls import path

from . import views
from . import dashboard_charts

app_name = 'data'
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('report', views.report, name='report'),
    path('result_detail', views.result_detail, name='result_detail'),
]
