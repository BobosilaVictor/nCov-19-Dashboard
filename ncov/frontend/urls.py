from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home-core'),
    path('daily/', views.daily, name= 'daily_report'),
]
