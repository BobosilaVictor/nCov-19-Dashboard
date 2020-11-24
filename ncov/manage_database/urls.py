from django.urls import path

from .views import county_upload


urlpatterns = [
    path('upload-csv/', county_upload, name='county_upload'),
]
