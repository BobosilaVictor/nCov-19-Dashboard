from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from .models import County, DailyReport
import pandas as pd


# Create your views here.


@permission_required('admin.can_add_log_entry')
def county_upload(request):
    template = "county_upload.html"

    prompt = {
        'order': 'Order of the CSV should be County name, latitude, longitude'
    }

    if request.method == 'GET':
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Not a csv file!')
    file = pd.read_csv(csv_file.name)

    for row in file.values:
        print(row[0], row[1], row[2])
        County.objects.update_or_create(
            name=row[0],
            latitude=row[1],
            longitude=row[2],
        )
    context = {}
    return render(request, template, context)


@permission_required('admin.can_add_log_entry')
def daily_upload(request):
    template = "county_upload.html"
    # Judet,Numar de cazuri confirmate(total),Numar de cazuri nou confirmate,Incidenta  inregistrata la 14 zile,Date
    prompt = {
        'order': 'Order of the CSV should be County name,number of cases, number of new cases, incidence, date'
    }

    if request.method == 'GET':
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Not a csv file!')
    file = pd.read_csv(csv_file.name)
    for row in file.values:
        County.objects.update_or_create(
            countyName=row[0],
            confirmedCases=row[1],
            newCases=row[2],
            incidence=row[3],
            date=row[4],
        )
    context = {}
    return render(request, template, context)
