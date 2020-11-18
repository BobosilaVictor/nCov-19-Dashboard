from django.test import TestCase

# Create your tests here.

from .models import County
import csv


def UploadCsvData():
    with open('getData/coordonateTari.csv', 'r', encoding='utf8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i in csv_reader:

            name, lat, long = i.split(sep=',')
            c = County(name, lat, long)
            try:
                c.save()
            except():
                # if the're a problem anywhere, you wanna know about it
                print("there was a problem with line")
