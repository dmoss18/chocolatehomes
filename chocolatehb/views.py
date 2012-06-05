from django.shortcuts import render_to_response, get_object_or_404
from chocolatehb.models import House

# Create your views here.
def index(request):
    house_data = House.objects.all()
    return render_to_response('index.html', {'house_data': house_data})

def upload_images(request, option_id):
    return render_to_response('admin/upload_images.html', {})
