from django.db import models
import datetime

# Create your models here.
class County(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()


class DailyReport(models.Model):
    countyName = models.ForeignKey(County, on_delete=models.PROTECT)
    confirmedCases = models.IntegerField()
    newCases = models.IntegerField()
    incidence = models.FloatField()
    date = models.DateField(default=datetime.datetime.today().strftime('%d-%m-%Y'))
