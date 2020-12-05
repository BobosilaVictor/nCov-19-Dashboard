from django.db import models
import datetime


# Create your models here.
class County(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()


class DailyReport(models.Model):
    countyName = models.CharField(max_length=100)
    confirmedCases = models.IntegerField()
    newCases = models.IntegerField()
    incidence = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False, blank=True,
                            default=datetime.datetime.now().strftime("%Y-%m-%d"))
    def __str__(self):
        return "{}, {}".format(self.countyName, self.date)
