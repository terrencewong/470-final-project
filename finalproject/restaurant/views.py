from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import generic
from django.utils import timezone

from .models import Order, MenuItem
from .forms import OrderStartForm

def index(request):
    return HttpResponse("Hello Group 4: Here is the empty project site.")

#def server(request):
#    return HttpResponse("Hello Server: Here is your home page")

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
    #def get_queryset(self):
    #    return Order.objects.get(pk=Order.id)
