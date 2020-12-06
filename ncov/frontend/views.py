from django.shortcuts import render, HttpResponse
from django.core import serializers
# Create your views here.
from .map import romania_map

import json

from django.apps import apps

def home(request):
    plot_div = romania_map()
    return render(request, template_name='frontend/index.html', context={'romania_map':plot_div})



def daily (request):

    county = apps.get_model('manage_database', 'County')
    daily_rep = apps.get_model('manage_database', 'DailyReport')

    data = county.objects.all()
    report = daily_rep.objects.all()

    data_c = serializers.serialize('json', data)
    report_c = serializers.serialize('json', report)


    data_c_json = json.loads(data_c)

    reprot_c_json = json.loads(report_c)



    json1 = json.dumps(data_c_json)
    json2 = json.dumps(reprot_c_json)


    json2

    return HttpResponse(json2, content_type="application/json")
