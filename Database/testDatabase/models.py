from django.db import models
from django_mysql.models import Model


# Create your models here.

class County(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    latitude = models.IntegerField()
    longitude = models.IntegerField()


class DailyReport(models.Model):
    countyName = models.ForeignKey(County, on_delete=models.PROTECT)
    confirmedCases = models.IntegerField()
    newCases = models.IntegerField()
    incidence = models.FloatField()
