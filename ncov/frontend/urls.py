from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home-core'),
    path('daily_report/', views.daily_report, name='daily_report'),
    path('realtime_growth/', views.realtime_growth, name='realtime_growth')

]
