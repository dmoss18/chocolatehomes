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
	#if user:
		#response['Content-Type'] = 'text/plain'
		#response.write('Hello, ' + user.nickname())
	return render_to_response('index.html', {'house_data': house_data, 'user': user})
	#else:
		#return redirect(users.create_login_url(request.path))
		#return render_to_response('index.html', {'house_data': house_data })
	
	#return render_to_response('index.html', {'house_data': house_data, 'user': user})
	#return response

def upload_images(request, option_id):
	return render_to_response('admin/upload_images.html', {})

def dashboard(request):
	user = users.get_current_user()
	#logger.info("user email is: " + user.email)
	
	if not user:
		logger.info("Path is " + request.path)
		return redirect(users.create_login_url(request.path))

	c = Client.objects.filter(email=user.email())
	if c:
		logger.info("In dashboard, if client" + request.path)
		house_data = House.objects.filter(client=c)
		return render_to_response('dashboard.html', {'house_data': house_data, 'user': user})
	else:
		return redirect('/welcome.html')

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

def new_house(request):
	user = users.get_current_user()
	if request.method == 'POST': # If the form has been submitted...
		form = HouseForm(request.POST) # A form bound to the POST data
		logger.info("houseform has data")
		if form.is_valid(): # All validation rules pass
			# Process the data in form.cleaned_data
			logger.info("houseform is valid")
			h = form.save(commit=False)
			h.client = Client.objects.get(email=user.email())
			h.save()
			
			#populate_house_defaults(h)
			
			cat = Category.objects.get(order=1)
			logger.info("category is " + cat.name)
			customization = Customization.objects.get(category=cat, order=1)
			logger.info("customization is " + customization.name)
			return redirect('/chocolatehb/house/' + str(h.id) + '/customizations/' + str(customization.id)) # Redirect after POST
	else:
		logger.info("houseform has no data.  Creating from instance")
		form = HouseForm() # An unbound form

	return render_to_response('chocolatehb/house/new.html', { 'houseForm': form, 'user': user}, context_instance=RequestContext(request))

def select_customization(request, house_id, customization_id):
	user = users.get_current_user()
	logger.info("in select_customization")
	cust = Customization.objects.get(pk=customization_id)
	options = Option.objects.filter(customization=cust)
	houseOption = HouseOption.objects.get(house=house_id,customization_id=cust.id)
	
	if request.method == 'POST': # If the form has been submitted...
		form = HouseOptionForm(request.POST)
		logger.info("form is created")
		if form.is_valid():
			logger.info("form is valid")
			houseOption.option = form.save(commit=False).option
			houseOption.selected = True
			houseOption.save()
			
			cust_array = Customization.objects.filter(category=cust.category)
			if(cust_array[len(cust_array)-1].id == cust.id):
				#We are on the last customization in this category
				#So we need to pull the first customization from the next category
				if(cust.category.order == 1):
					#User just saved last customization of a new house (1st category)
					#So we send them back to a generic page
					return redirect('/chocolatehb/house/' + str(house_id))
				cat_array = Category.objects.filter(order=cust.category.order + 1)
				if(cat_array):
					#There is another category, so we pull the next one
					cat = Category.objects.get(order=cust.category.order+1)
					cust = Customization.objects.get(category=cat,order=1)
					return redirect('/chocolatehb/house/' + str(house_id) + '/customizations/' + str(cust.id))
				else:
					#We hit the last category, so we need to navigate somewhere else
					return redirect('/chocolatehb/house/' + str(house_id))
			else:
				cust = Customization.objects.get(category=cust.category,order=cust.order + 1)
				return redirect('/chocolatehb/house/' + str(house_id) + '/customizations/' + str(cust.id))

	page_type = "full_page"

	if cust.page_type.name == 'Tile Page':
		#render tile_page template
		page_type = "tile_page"
	elif cust.page_type.name == 'Pallette Page':
		#render pallette_page template
		page_type = "pallette_page"
	
	
	return render_to_response('chocolatehb/customizations/' + page_type + '_customization.html', { 'user': user, 'customization': cust, 'options': options, 'house_id': house_id, 'selectedHouseOption': houseOption }, context_instance=RequestContext(request))
	
def show_house(request, house_id):
	house = House.objects.get(pk=house_id)
	return render_to_response('chocolatehb/house/show.html', { 'house': house, 'options': house.options.all().order_by('customization__category') })
