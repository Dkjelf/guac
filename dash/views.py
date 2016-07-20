from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from datetime import datetime
from .forms import UserForm, UserProfileForm

@login_required
def index(request):
	context = RequestContext(request)	

	# Cookie information
	# Obtain the response object early to add cookie information
	response = render(request, 'dash/guac_scrape.html', context)

	# Get the number of visits to the site
	visits = int(request.COOKIES.get('visits', '0'))

	# Does the cookie last_visit exist?
	if 'last_visit' in request.COOKIES:
		#Yes
		last_visit = request.COOKIES['last_visit']
		# Cast the value to a date/time object
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

		# If it's been more than one day
		if (datetime.now() - last_visit_time).days > 0:
			# reassign the value of the cookie to +1
			response.set_cookie('visits', visits+1)
			response.set_cookie('last_visit', datetime.now())
	else:
		# Cookie last_visit doesn't exist, so create current date/time
		response.set_cookie('last_visit', datetime.now())

	# Return response back to the user, updating any cookies that need changed.
	return response	
		

	
	return render(request, 'dash/guac_scrape.html')

def home(request):
	# Displays the home page
	return render(request, 'dash/home.html')


def about(request):
	# Displays the about page
	return render(request, 'dash/about.html')

def register(request):
	# Like before, get the request's context.
	context = RequestContext(request)

	# A boolean value for telling the template whether the registration was successful.
	# Set to False initially. Code changes value to True when registration succeeds.
	registered = False	
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			#Save the user's form data to the database
			user = user_form.save()
			
			# Now hash the password and update the user object
			user.set_password(user.password)
			user.save()
			
			# Sort out the UserProfile instance. 
			profile = profile_form.save(commit=False)
			profile.user = user

			# If the user chose to upload an image...
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			# Now save the UserProfile model instance
			profile.save()

			# Update variable to confirm that the user is registered
			registered = True
	
			return render(request, 'dash/login.html', context)
		# Invalid form or forms with mistakes
		# Prints the errors to terminal and shows it to the user
		else:
			print user_form.errors, profile_form.errors
	# Not an HTTP POST, so we render our form using two ModelForm instances.
	# These forms will be blank, ready for user input.
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	# Render the template depending on the context
	return render(request,
		'dash/register.html',
		{'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
		 context)

def user_login(request):
	#obtain context
	context = RequestContext(request)

	# If the request is an HTTP POST, try to pull out the relevant information
	if request.method == "POST":
		# Gather the username and password provided by the user
		username = request.POST['username']
		password = request.POST['password']

		# Authenticate if the username/password combo is valid
		user = authenticate(username=username, password=password)

		if user:
			# Check if the account is active
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/dash/')
			else:
				# Responds to an inactive account
				return HttpResponse("This Guac acccount is inactive. Please contact an administrator.")
		else:
			# Bad login details
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details, try again.")
	# This request is not an HTTP POST, so display the form
	else: 
		# No Context variables to pass the template system
		return render(request, 'dash/login.html', context)
		
	
@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/dash/')

@login_required
def get_user_profile(request):
	context = RequestContext(request)
	context_dict = {}
	u = User.objects.get(username = request.user)

	try:
		up = UserProfile.objects.get(user=u)	
	except:
		up = None	
	
	context_dict['user'] = u
	context_dict['userprofile'] = up
	return render(request,'dash/user_profile.html', context_dict, context)
