from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from .models import Table, Order, MenuItem, Alert, OrderedMenuItems, UserType
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils import timezone
from .forms import OrderStartForm, LoginForm, TableIDForm, KitchenForm, OrderForm, ItemForm, ContactServerForm
from django.contrib.auth.decorators import login_required
from restaurant.models import UserType
from .forms import OrderStartForm, LoginForm, TableIDForm, KitchenForm
from menu.models import menu
from restaurant.models import UserType
from django.views.generic.detail import SingleObjectMixin


def home(request):
    return render(request, 'restaurant/home.html')

def index(request):
    return HttpResponse("Hello Group 4: Here is the empty project site.")

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
				#reverse_url = reverse('OrderNow')
				#return HttpResponseRedirect(reverse_url)
				return HttpResponseRedirect('/index/order/')
				#return HttpResponse("This exists.")
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
	if user.usertype.is_customer :
		is_customer = True
	else:
		is_customer = False

	if user.usertype.is_kitchen :
		is_kitchen = True
	else:
		is_kitchen = False

	if user.usertype.is_server :
		is_server = True
	else:
		is_server = False
	context = {
		'username':username,
		'is_customer': is_customer,
		'is_kitchen': is_kitchen,
		'is_server': is_server,
	}
	return render(request, 'restaurant/gateway.html', context)

class KitchenView(generic.ListView):
	template_name = 'restaurant/kitchen.html'
	context_object_name = 'order_list'
	
	def get_queryset(self):
		return Order.objects.all().exclude(Status ='CREATED').exclude(Status ='COMPLETED').exclude(Status ='SERVED').order_by('Table')
		
	template_name = 'restaurant/kitchen.html'
	context_object_name = 'order_list'
	def get_queryset(self):
		return Order.objects.all().filter(Status='SENT TO KITCHEN').order_by('Table')

def kitchendetail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        form = KitchenForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('restaurant:kitchen'))
    else:
        form = KitchenForm(instance=order)
    return render(request, 'restaurant/kitchendetail.html', {'form':form, 'order':order})

def gateway(request,username):         # gate way is added for users who has multiple roles (might be dropped later)
	user=get_object_or_404(User.objects, username=username)
	if user.usertype.is_customer:
		return render(request, 'restaurant/gateway.html', {'username':username})

#Main Kitchen View
class KitchenView(generic.ListView):
    template_name = 'restaurant/kitchen.html'
    context_object_name = 'order_list'
    def get_queryset(self):
        return Order.objects.all().exclude(Status ='CREATED').exclude(Status ='COMPLETED').exclude(Status ='SERVED').order_by('Table')

#Kitchen's view of each table's order
def kitchendetail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        form = KitchenForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            if order.Status == 'READY':
                alert = Alert.objects.create(Order=order, Message='Meal ready', Resolved=0)
            return HttpResponseRedirect(reverse('restaurant:kitchen'))
    else:
        form = KitchenForm(instance=order)
    return render(request, 'restaurant/kitchendetail.html', {'form':form, 'order':order})


#View for the account creation page:
def createaccount(request):
    error = False
    originalUserInputs = {}

    if (('username' in request.POST) and ('emailaddress' in request.POST) and ('firstname' in request.POST) and ('surname' in request.POST) and ('password' in request.POST) and ('reenterpassword' in request.POST)):
        username = request.POST['username']
        emailaddress = request.POST['emailaddress']
        firstname = request.POST['firstname']
        surname = request.POST['surname']
        password = request.POST['password']
        reenterpassword = request.POST['reenterpassword']

        if ((not username) or (not emailaddress) or (not firstname) or (not surname) or (not password) or (not reenterpassword)):
            error = True

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
        else:
            return HttpResponse("Data entered into DB")

    originalUserInputs['error'] = error

    return render(request, 'restaurant/createaccount.html', originalUserInputs)
