from django.shortcuts import render

# Create your views here.
from .map import romania_map

def home(request):
    plot_div = romania_map()
    return render(request, template_name='frontend/index.html', context={'romania_map':plot_div})
