from django.shortcuts import render, HttpResponse
from django.core import serializers
# Create your views here.
from .map import romania_map

import json

from django.apps import apps


def home(request):
    plot_div = romania_map()
    return render(request, template_name='frontend/index.html', context={'romania_map': plot_div})


def daily(request):
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
