from django.shortcuts import render
import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from .models import County, DailyReport


# Create your views here.


@permission_required('admin.can_add_log_entry')
def county_upload(request):
    template = "county_upload.html"

    prompt = {
        'order': 'Order of the CSV should be County name, latitude, longitude'
    }

    if request.method == 'GET':
        return render(request, template, prompt)

    csv_file = request.FILES('file')

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Not a csv file!')

    file = pd.read_csv(csv_file)
    for row in file.values:
        obj = County.objects.update_or_create(
            name=row[0],
            latitude=row[1],
            longitude=row[2],
        )
    context = {}
    return render(request, template, context)
