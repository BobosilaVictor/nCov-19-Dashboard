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
    # data_set = csv_file.read().decode('UTF-8')
    # io_string = io.StringIO(data_set)
    # next(io_string)
    # for column in csv.reader(io_string, delimiter=',', quotechar="|"):
    #     _, created = County.objects.update_or_create(
    #         name=column[0],
    #         latitude=column[1],
    #         longitude=column[2],
    #     )
    file = pd.read_csv(csv_file.name)

    for row in file.values:
        print(row[0],row[1],row[2])
        County.objects.update_or_create(
            name=row[0],
            latitude=row[1],
            longitude=row[2],
                )
    context = {}
    return render(request, template, context)
