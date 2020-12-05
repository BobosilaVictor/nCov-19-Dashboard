from django.urls import path

from .views import county_upload, daily_upload


urlpatterns = [
    path('upload-csv/', county_upload, name='county_upload'),
    path('upload-daily/', daily_upload, name='daily_upload'),
]
