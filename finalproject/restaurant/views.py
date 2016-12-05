from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin
from django.db import IntegrityError  #Needed for the account-creation page. See the createaccount() function below.

from .forms import OrderStartForm, LoginForm, TableIDForm, KitchenForm, OrderForm, ItemForm, ContactServerForm
from restaurant.models import UserType
from .models import Table, Order, Alert, OrderedMenuItems, UserType, Payment
from menu.models import menu

from django.views.generic.detail import SingleObjectMixin
from django.db import IntegrityError  #Needed for the account-creation page. See the createaccount() function below.
from django.views.decorators.csrf import csrf_exempt
import stripe


def home(request):
	return render(request, 'restaurant/home.html')

def welcome(request):
	return render(request, 'restaurant/welcome.html')
	#return HttpResponse("Welcome.")

#Customer Input - verify customer's order code has been created by server
def TableIDVerification(request):
	if request.POST:
		form = TableIDForm(request.POST)
		if form.is_valid():
			code_id = form.data['Code']
			request.session['Code'] = code_id
			try:
				p = Order.objects.get(Code=code_id)
				return HttpResponseRedirect('/menu/')
				#return HttpResponse("This exists.")
			except Order.DoesNotExist:
				#return HttpResponse("This code does not exist. Please try again.")
				return HttpResponseRedirect('/guest-user/tryagain')
			except Order.DoesNotExist:
				return HttpResponse("This code does not exist. Please try again.")
	else:
		form = TableIDForm()
	if request.GET.get('table', ''):
		table = Table.objects.get(id=request.GET.get('table', ''))
	variables = {
		'form': form,
	}
	template = 'restaurant/TableIDVerificationForm.html'
	return render(request, template, variables)

# if order code does not exist
def TryAgain(request):
	return render(request, 'restaurant/tryagain.html')

class MenuView(generic.ListView):
	template_name = 'restaurant/menu.html'
	context_object_name = 'latest_menuitem_list'

	def get_context_data(self, *args, **kwargs):
		context = super(MenuView, self).get_context_data(*args, **kwargs)
		code = self.request.session['Code']
		pk = Order.objects.get(Code=code)
		context['current_menu_items'] = OrderedMenuItems.objects.filter(order_id=pk)
		return context

	def get_queryset(self):
		return menu.objects.all().order_by('Name')

def AddItem(request, pk):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		current_item = menu.objects.get(id=pk)

		request.session['Name']=current_item.Name
		request.session['Description']=current_item.Description
		request.session['Nutrition']=current_item.Nutrition
		request.session['Price']=current_item.Price

		pre_form = OrderForm(instance=current_item)
		form = ItemForm(request.POST)
		# check whether it's valid:

		if form.is_valid() and (form.cleaned_data['num_items'] >0):
			Code=request.session['Code']
			order_id = Order.objects.get(Code=Code)
			item_name=current_item
			num_items=form.cleaned_data['num_items']
			notes=form.cleaned_data['notes']
			item = OrderedMenuItems.objects.create(order_id=order_id, item_name=item_name, num_items=num_items, notes=notes)

			temp_total = num_items * current_item.Price
			if Payment.objects.filter(pay_id=order_id).exists():
				current_total = Payment.objects.get(pay_id=order_id)
				add_to_total = current_total.total + temp_total
				Payment.objects.update(pay_id=order_id, total=add_to_total)
			else:
				Payment.objects.create(pay_id=order_id, total=temp_total)
			return HttpResponseRedirect('/menu/')

		# don't order item if num_items = 0
		else:
			return HttpResponseRedirect('/menu/')

	# if a GET (or any other method) we'll create a blank form

	else:
		current_item = menu.objects.get(id=pk)

		request.session['Name']=current_item.Name
		request.session['Description']=current_item.Description
		request.session['Nutrition']=current_item.Nutrition
		request.session['Price']=current_item.Price
		pre_form = OrderForm(instance=current_item)
		form = ItemForm()

		return render(request, 'restaurant/additem.html', {'form': form})

# display order status and contact server option
def orderplaced(request):
	Code = request.session['Code']
	if Order.objects.filter(Code=Code).filter(Status='CREATED').exists():
		Order.objects.filter(Code=Code).update(Status='SENT TO KITCHEN')
	order = get_object_or_404(Order, Code=Code)
	return render(request, 'restaurant/orderplaced.html', {'order':order})

#contact server form
def ContactServer(request):

	if request.POST:

		form = ContactServerForm(request.POST)

		if form.is_valid() and form.cleaned_data['Message']:

			Code=request.session['Code']
			order_id = Order.objects.get(Code=Code)
			message = form.cleaned_data['Message']
			alert = Alert.objects.create(Message=message, Order=order_id)

			return HttpResponseRedirect('/contact-server-sent/')

		else:
			return HttpResponseRedirect('/contact-server/')
	else:
		form = ContactServerForm()
		return render(request, 'restaurant/contactserver.html', {'form': form})

def ContactServerSent(request):
	return render(request, 'restaurant/contactserversent.html')

def ordernow(request):
	code = request.session['Code']
	menu_item_list = menu.objects.all()
	return render(request, 'restaurant/order-now.html', {'code':code, 'menu_item_list':menu_item_list})

class ServerView(generic.ListView):
	template_name = 'restaurant/server.html'
	context_object_name = 'current_alert_list'
	def get_queryset(self):
		return Alert.objects.filter(Resolved=0)#.order_by('Order_id.Table')

def StartOrder(request):
	# if this is a POST request we need to process the form data
	current_user = request.user
	user_id = current_user.id
	user_type = UserType.objects.get(user_id=user_id)
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = OrderStartForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			Code=form.cleaned_data['Code']
			Table=form.cleaned_data['Table']
			Restaurant=user_type.restaurant
			order = Order.objects.create(Code=Code, Table=Table, Restaurant=Restaurant, Status='CREATED', StartTime=timezone.now())
			return HttpResponseRedirect('/server/orderstart')
	# if a GET (or any other method) we'll create a blank form
	else:
		form = OrderStartForm()
	return render(request, 'restaurant/orderstart.html', {'form': form})

class OrderView(SingleObjectMixin, generic.ListView):

	template_name = 'restaurant/orders.html'
	context_object_name = 'latest_order_list'

	def get_object(self):
		return get_object_or_404(User, pk=request.session['user_id'])

	def get(self, request, *args, **kwargs):
		user = self.request.user
		current_user = user
		user_id = current_user.id
		user_type = UserType.objects.get(user_id=user_id)
		Restaurant=user_type.restaurant
		self.object = Order.objects.filter(Restaurant = Restaurant)
		return super(OrderView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(OrderView, self).get_context_data(**kwargs)
		context['orders'] = self.object
		return context

	def get_queryset(self):
		return self.object.all().order_by('Table')

class OrderDetailView(generic.DetailView):
	model = Order
	template_name = 'restaurant/orderdetail.html'

def orderdetail(request, order_id):
	order = get_object_or_404(Order, pk=order_id)
	if request.method == "POST":
		form = KitchenForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('restaurant:orders'))
	else:
		form = KitchenForm(instance=order)
	return render(request, 'restaurant/orderdetail.html', {'form':form, 'order':order})

class AlertDetailView(generic.DetailView):
	model = Alert
	template_name = 'restaurant/alertdetail.html'

def resolveAlert(request, alert_id):
	alert = get_object_or_404(Alert, pk=alert_id)
	alert.Resolved = 1
	alert.save()
	alert.delete()
	return HttpResponseRedirect(reverse('restaurant:server'))

# Authentication Views
def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				# the password verified for the user
				if user.is_active:
					print("User is valid, active and authenticated")
					login(request, user)
					return (render(request, 'restaurant/redirect.html', {'username':username} ))
				else:
					print("The password is valid, but the account has been disabled!")
			else:
				# the authentication system was unable to verify the username and password
				print("The username and password were incorrect.")
	else:
		form = LoginForm()
	return render(request, 'restaurant/login.html', {'form': form})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def gateway(request,username):         # gateway is added for users who has multiple roles (might be dropped later)
    user=get_object_or_404(User.objects, username=username)
    if user.usertype.is_customer:
        is_customer = True
    else:
        is_customer = False
        
    if user.usertype.is_kitchen:
        is_kitchen = True
    else:
        is_kitchen = False
        
    if user.usertype.is_server:
        is_server = True
    else:
        is_server = False

    if user.is_staff:
        is_staff = True
    else:
        is_staff = False
        
    context = {
        'username':username,
        'is_customer': is_customer,
        'is_kitchen': is_kitchen,
        'is_server': is_server,
        'is_staff': is_staff,
    }
    return render(request, 'restaurant/gateway.html', context)

#Main Kitchen View
class KitchenView(generic.ListView):
	template_name = 'restaurant/kitchen.html'
	context_object_name = 'order_list'
	def get_queryset(self):
		return Order.objects.all().exclude(Status ='CREATED').exclude(Status ='COMPLETED').exclude(Status ='SERVED').order_by('Table')

#Kitchen's view of each table's order
def kitchendetail(request, order_id):
	order = get_object_or_404(Order, pk=order_id)

	current_menu_items = OrderedMenuItems.objects.filter(order_id=order_id)

	if request.method == "POST":
		form = KitchenForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			if order.Status == 'READY':
				alert = Alert.objects.create(Order=order, Message='Meal ready', Resolved=0)
			return HttpResponseRedirect(reverse('restaurant:kitchen'))
	else:
		form = KitchenForm(instance=order)
	return render(request, 'restaurant/kitchendetail.html', {'form':form, 'order':order, 'current_menu_items':current_menu_items})

@csrf_exempt
def payment(request):
	Code=request.session['Code']
	pay_id = Order.objects.get(Code=Code)
	amount_due = Payment.objects.get(pay_id=pay_id)

	tax = 0.12 #set tax

	real_total = amount_due.total + (amount_due.total * tax)
	amount_due_converted_to_cents = int(real_total * 100)

	if request.method == "GET":
		return render(request, 'restaurant/payment.html', {'amount_due':amount_due, 'real_total':real_total})
	if request.method == "POST":
		stripe.api_key = "sk_test_BIY8Qzh7rZoB1A1Bl6o8GI9Q"
		token = request.POST['stripeToken']
		customer = stripe.Customer.create(
			source=token,
			description="test" #change later
		)
		stripe.Charge.create(
			amount=amount_due_converted_to_cents, # in cents
			currency="cad",
			customer=customer.id
		)
		return HttpResponseRedirect('/')

#View-function for the account-creation page:
def createaccount(request):
	#Template variables:
	fieldsDoNotExist = False
	userNameTaken = False
	retypedPasswordDoesNotMatch = False

	#Dictionary to hold template variables:
	originalUserInputs = {}

	#Check that all the expected form fields exist:
	if (('username' in request.POST) and ('emailaddress' in request.POST) and
		('firstname' in request.POST) and ('surname' in request.POST) and
		('password' in request.POST) and ('reenterpassword' in request.POST)):

		#Extract all the values from the form's fields:
		username = request.POST['username']
		emailaddress = request.POST['emailaddress']
		firstname = request.POST['firstname']
		surname = request.POST['surname']
		password = request.POST['password']
		reenterpassword = request.POST['reenterpassword']

		#Check if any of the fields contain an empty value:
		if ((not username) or (not emailaddress) or (not firstname) or
			(not surname) or (not password) or (not reenterpassword)):

			fieldsDoNotExist = True  #At least one field contains an empty value.

			#We will have to present the account-creation form to the user again
			#so that he/she can fill in just the fields that are still empty.
			#Figure out which of the form's fields were already filled in by
			#the user, so we can fill in those fields for the user and spare
			#the user some extra typing:
			if (username):
				originalUserInputs['username'] = username
			else:
				originalUserInputs['username'] = ''

			if (emailaddress):
				originalUserInputs['emailaddress'] = emailaddress
			else:
				originalUserInputs['emailaddress'] = ''

			if (firstname):
				originalUserInputs['firstname'] = firstname
			else:
				originalUserInputs['firstname'] = ''

			if (surname):
				originalUserInputs['surname'] = surname
			else:
				originalUserInputs['surname'] = ''

			if (password):
				originalUserInputs['password'] = password
			else:
				originalUserInputs['password'] = ''

			if (reenterpassword):
				originalUserInputs['reenterpassword'] = reenterpassword
			else:
				originalUserInputs['reenterpassword'] = ''

		#All the fields are filled in, but we need to check if the re-typed
		#password matches the password the user first typed:
		elif (password != reenterpassword):
			retypedPasswordDoesNotMatch = True  #The re-typed password does NOT match the password the user first typed.

			originalUserInputs['retypedPasswordDoesNotMatch'] = retypedPasswordDoesNotMatch
			originalUserInputs['fieldsDoNotExist'] = fieldsDoNotExist
			originalUserInputs['userNameTaken'] = userNameTaken

			originalUserInputs['username'] = username
			originalUserInputs['emailaddress'] = emailaddress
			originalUserInputs['firstname'] = firstname
			originalUserInputs['surname'] = surname

			#Blanking both the Password and Re-enter password fields to make
			#the user enter the password into both fields again:
			originalUserInputs['password'] = ''
			originalUserInputs['reenterpassword'] = ''

			return render(request, 'restaurant/createaccount.html', originalUserInputs)

		#Create the user's account...
		else:
			#Create the user's account by creating a record in the User table
			#with all the user's information:
			try:
				User.objects.create_user( username = username,
										  first_name = firstname,
										  last_name = surname,
										  email = emailaddress,
										  password = password,
										  is_staff = False,
										  is_active = True,
										  is_superuser = False
										)
			#The username chosen by the user has to be unique. If it's not
			#unique, this exception gets thrown, so we will have to ask the
			#user to choose a different username. We will present the account-
			#creation form to the user again, but with all the fields, except
			#the username field, filled in with his/her original entries:
			except IntegrityError:
				userNameTaken = True
				originalUserInputs['userNameTaken'] = userNameTaken
				originalUserInputs['fieldsDoNotExist'] = fieldsDoNotExist
				originalUserInputs['retypedPasswordDoesNotMatch'] = retypedPasswordDoesNotMatch

				originalUserInputs['username'] = ''  #Blanking the username field.
				originalUserInputs['emailaddress'] = emailaddress
				originalUserInputs['firstname'] = firstname
				originalUserInputs['surname'] = surname
				originalUserInputs['password'] = password
				originalUserInputs['reenterpassword'] = reenterpassword

				return render(request, 'restaurant/createaccount.html', originalUserInputs)
			#The record representing the user's new account was successfully
			#created and inserted into the User table:
			else:
				return render(request, 'restaurant/createaccount_successful.html')

	#At least one of the expected form fields does NOT exist:
	originalUserInputs['fieldsDoNotExist'] = fieldsDoNotExist

	originalUserInputs['userNameTaken'] = userNameTaken
	originalUserInputs['retypedPasswordDoesNotMatch'] = retypedPasswordDoesNotMatch
	return render(request, 'restaurant/createaccount.html', originalUserInputs)
