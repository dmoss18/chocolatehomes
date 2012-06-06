from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from chocolatehb.models import *
from django.template import RequestContext
from django.core.exceptions import ValidationError
from google.appengine.api import users
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    house_data = House.objects.all()
    user = users.get_current_user()
    
    #response = HttpResponse()
    if user:
        #response['Content-Type'] = 'text/plain'
        #response.write('Hello, ' + user.nickname())
        return render_to_response('dashboard.html', {'house_data': house_data, 'user': user, 'greeting': 'Hello, ' + user.nickname()})
    else:
        #return redirect(users.create_login_url(request.path))
        return render_to_response('index.html', {'house_data': house_data })
    
    #return render_to_response('index.html', {'house_data': house_data, 'user': user})
    #return response

def upload_images(request, option_id):
    return render_to_response('admin/upload_images.html', {})

def dashboard(request):
    house_data = House.objects.all()
    user = users.get_current_user()
    client = Client.objects.filter( email=user.email() )
    logger.info("user email is: " + request.user.email)
    
    if not client:
        return redirect('/welcome.html')
    
    if user:
        return render_to_response('dashboard.html', {'house_data': house_data, 'user': user})
    else:
        return redirect('index.html')

def welcome(request):
    user = users.get_current_user()
    logger.info("In welcome view")

    if request.method == 'POST': # If the form has been submitted...
        form = ClientForm(request.POST) # A form bound to the POST data
        logger.info("form has data")
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            logger.info("form is valid")
            c = form.save(commit=False)
            c.email = user.email()
            c.username = user.nickname()
            c.google_id = user.user_id()
            c.save()
            return redirect('/dashboard.html/') # Redirect after POST
    else:
        logger.info("form has no data.  Creating from instance")
        form = ClientForm() # An unbound form

    return render_to_response('welcome.html', { 'clientForm': form, 'user': user}, context_instance=RequestContext(request))

