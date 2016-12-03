from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from .forms import TableIDForm, OrderForm
from .models import Table, Order, MenuItem, OrderedMenuItems
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.utils import timezone
from .forms import OrderStartForm, LoginForm, ItemForm
from menu.models import menu
#from django.forms import formset_factory

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

				return HttpResponseRedirect('/index/menu/')

				#reverse_url = reverse('OrderNow')
				#return HttpResponseRedirect(reverse_url)
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
        if form.is_valid():
            
            Code=request.session['Code']
            order_id = Order.objects.get(Code=Code)
            item_name=current_item
            num_items=form.cleaned_data['num_items']
            notes=form.cleaned_data['notes']
            item = OrderedMenuItems.objects.create(order_id=order_id, item_name=item_name, num_items=num_items, notes=notes)
            
            return HttpResponseRedirect('/index/menu/')

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

def ordernow(request):

	#timestamp

	form = OrderForm()
	#code = request.session['Code']
	menu_item_list = menu.objects.all()
	#order = Order.objects.get(Code=code)

	if request.method == "GET":
		form = OrderForm(
			initial = {

				'order_id' : request.session['Code'],
				#'table_id' : order.Table,
				#'item_name' : menu.Name,				
			},
		)

		return render(request, 'restaurant/order-now.html', {'menu_item_list':menu_item_list, 'form' : form})


	elif request.method == "POST":

		#if form.is_valid():

		for item_name in request.POST.getlist('item_name'):

			itemform = OrderForm(request.POST)
			form = OrderForm({'item_name': item_name}, instance=OrderedMenuItems())

			code_id = itemform.data['order_id']
			order_code = Order.objects.get(Code=code_id)

			#table_id = form.cleaned_data['table_id']
			item_name = form.data['item_name']
			item_code = menu.objects.get(Name=item_name)
			num_items = itemform.data['num_items']
			notes = itemform.data['notes']
			#form.save()

			OrderedMenuItems.objects.create(order_id=order_code, item_name=item_code, num_items=num_items, notes=notes)
            #OrderedMenuItems.objects.create(order_id=order_code, item_name=item_code, num_items=num_items, notes=notes)
            
            
			#, item_name=item_name, num_items=num_items, notes=notes)
			#return HttpResponse("yes.")


		return HttpResponseRedirect('/index/welcome/')
		#return HttpResponse(order_code)
		#else:

			#template = 'restaurant/order_now.html'
			#return render(request, template, variables)
			#return HttpResponse("no.")
			#return render(request, 'restaurant/order-now.html', {'menu_item_list':menu_item_list, 'form' : form})
			#form = OrderForm()

	#template = 'restaurant/order-now.html'
	#return render(request, template, {'menu_item_list':menu_item_list, 'form': form})
		#'code':code,
		#return HttpResponse("you're done.")


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
            order = Order.objects.create(Code=Code, Table=Table, Completed=0, StartTime=timezone.now())
            return HttpResponseRedirect('/index/server/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = OrderStartForm()

    return render(request, 'restaurant/server.html', {'form': form})

class OrderView(generic.ListView):
    template_name = 'restaurant/orders.html'
    context_object_name = 'latest_order_list'
    def get_queryset(self):
        return Order.objects.filter(Completed=0).order_by('Table')

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

class KitchenView(TemplateView):
   template_name = 'restaurant/kitchen.html'
   order_list = Order.objects.all()

class KitchenDetailView(generic.DetailView):
    model = Order
    template_name = 'restaurant/kitchendetail.html'
