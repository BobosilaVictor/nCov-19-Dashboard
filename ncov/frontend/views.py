from django.shortcuts import render, HttpResponse
from django.core import serializers
import datetime
import platform

import pandas as pd

# Create your views here.


import json

from django.apps import apps

STRFTIME_DATA_FRAME_FORMAT = '%#m/%#d/%y'


def home(request):
    return render(request, template_name='frontend/index.html')


def daily_report(request):
    county = apps.get_model('manage_database', 'County')
    daily_rep = apps.get_model('manage_database', 'DailyReport')

    data = county.objects.all()
    report = daily_rep.objects.all()

    data_c = serializers.serialize('json', data)
    report_c = serializers.serialize('json', report)

    data_c_json = json.loads(data_c)

    report_c_json = json.loads(report_c)

    dict_final = {}
    # key: lat, long, pk, confirmed cases, nou, incidenta, data

    dict_lat = {}
    dict_long = {}
    dict_pk = {}
    dict_conf = {}
    dict_nou = {}
    dict_incidenta = {}
    dict_dates = {}

    for i in range(0, len(data_c_json)):
        dict_lat[str(i)] = str(data_c_json[i]['fields']['latitude'])
    for i in range(0, len(data_c_json)):
        dict_long[str(i)] = str(data_c_json[i]['fields']['longitude'])
    for i in range(0, len(data_c_json)):
        dict_pk[str(i)] = str(data_c_json[i]['pk'])
    for i in range(0, len(report_c_json)):
        dict_conf[str(i)] = str(report_c_json[i]['fields']['confirmedCases'])
    for i in range(0, len(report_c_json)):
        dict_nou[str(i)] = str(report_c_json[i]['fields']['newCases'])
    for i in range(0, len(report_c_json)):
        dict_incidenta[str(i)] = str(report_c_json[i]['fields']['incidence'])
    for i in range(0, len(report_c_json)):
        dict_dates[str(i)] = str(report_c_json[i]['fields']['date'])

    dict_final['lat'] = dict_lat
    dict_final['long'] = dict_long
    dict_final['pk'] = dict_pk
    dict_final['conf'] = dict_conf
    dict_final['nou'] = dict_nou
    dict_final['incidenta'] = dict_incidenta
    dict_final['dates'] = dict_dates

    dict_final_json = json.dumps(dict_final)

    return HttpResponse(dict_final_json, content_type="application/json")


def growth(date_string=None, weekly=False, monthly=False):
    daily_rep = apps.get_model('manage_database', 'DailyReport')
    report = daily_rep.objects.all()
    report_c = serializers.serialize('json', report)
    report_c_json = json.loads(report_c)
    dict_final={}
    dict_conf={}

    for i in range(0, len(report_c_json)):
        dict_conf[report_c_json[i]['fields']['date']] = str(report_c_json[i]['fields']['confirmedCases'])

    growth_df = pd.DataFrame(data=dict_conf)
    print(growth_df)
    growth_df.index = growth_df.index.rename('Date')

    yesterday = pd.Timestamp('now').date() - pd.Timedelta(days=1)
    print(growth_df)
    if date_string is not None:
        return growth_df.loc[growth_df.index == date_string]

    if weekly is True:
        weekly_df = pd.DataFrame([])
        intervals = pd.date_range(end=yesterday, periods=8, freq='7D').strftime(STRFTIME_DATA_FRAME_FORMAT).tolist()
        for day in intervals:
            weekly_df = weekly_df.append(growth_df.loc[growth_df.index == day])
        return weekly_df

    elif monthly is True:
        monthly_df = pd.DataFrame([])
        intervals = pd.date_range(end=yesterday, periods=3, freq='1M').strftime(STRFTIME_DATA_FRAME_FORMAT).tolist()
        for day in intervals:
            monthly_df = monthly_df.append(growth_df.loc[growth_df.index == day])
        return monthly_df

    return growth_df


def realtime_growth(request):
    df = growth()

   # df.index = pd.to_datetime(df.index)
   # df.index = df.index.strftime('%Y-%m-%d')

    return HttpResponse(df.to_json(orient='columns'), content_type='application/json')
