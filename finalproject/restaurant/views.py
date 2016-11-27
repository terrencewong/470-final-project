from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from .forms import TableIDForm
from .models import Table, Order, MenuItem
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.utils import timezone
from .forms import OrderStartForm, LoginForm, KitchenForm
from menu.models import menu

def index(request):
    return HttpResponse("Hello Group 4: Here is the empty project site.")

def welcome(request):
	return render(request, 'restaurant/welcome.html')
	#return HttpResponse("Welcome.")

#def TableIDVerification(request):
	#return render(request, 'restaurant/TableIDVerificationForm.html')

def TableIDVerification(request):
	if request.POST:
		form = TableIDForm(request.POST)
		if form.is_valid():
			code_id = form.data['Code']
			request.session['Code'] = code_id
			try:
				p = Order.objects.get(Code=code_id)
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

def ordernow(request):
	code = request.session['Code']
	menu_item_list = menu.objects.all()
	return render(request, 'restaurant/order-now.html', {'code':code, 'menu_item_list':menu_item_list})

class ServerView(TemplateView):
    template_name = 'restaurant/server.html'

def StartOrder(request):
    # if this is a POST request we need to process the form data
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
            order = Order.objects.create(Code=Code, Table=Table, Status='CREATED', StartTime=timezone.now())
            return HttpResponseRedirect('/index/server/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = OrderStartForm()
    return render(request, 'restaurant/server.html', {'form': form})

class OrderView(generic.ListView):
    template_name = 'restaurant/orders.html'
    context_object_name = 'latest_order_list'
    def get_queryset(self):
        return Order.objects.all().order_by('Table')

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'restaurant/orderdetail.html'

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
                    return HttpResponseRedirect('/index')
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
    return HttpResponseRedirect('/index')

class KitchenView(generic.ListView):
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
