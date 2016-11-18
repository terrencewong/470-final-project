from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
<<<<<<< HEAD
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Order, MenuItem
from .forms import OrderStartForm, LoginForm

def index(request):
    return HttpResponse("Hello Group 4: Here is the empty project site.")

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
=======
from django.views import generic
from django.utils import timezone

from .models import Order

def index(request):
   return HttpResponse("Hello Group 4: Here is the empty project site.")

class KitchenView(TemplateView):
   template_name = 'restaurant/kitchen.html'
   order_list = Order.objects.all()

class KitchenDetailView(generic.DetailView):
    model = Order
    template_name = 'restaurant/kitchendetail.html'
>>>>>>> origin/terrence-kitchen
