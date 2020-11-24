from django.contrib import admin

# Register your models here.

from .models import County, DailyReport

admin.site.register(County)
admin.site.register(DailyReport)
