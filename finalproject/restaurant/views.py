from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
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
