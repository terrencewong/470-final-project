# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse
from .models import menu

def index(request):

	latest_menu_list = menu.objects.order_by('-id')[:1000]
   	template = loader.get_template('menu/index.html')
   	context = {
        'latest_menu_list': latest_menu_list,
    	}
    	return HttpResponse(template.render(context, request))



def detail(request, menu_id):
    question = get_object_or_404(menu, pk=menu_id)
    return render(request, 'menu/detail.html', {'question': question})


def results(request, menu_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % menu_id)

def display(request):
  return render_to_response('index.html', {'obj': models.menu.objects.all()})

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from .models import menu as Users
from .forms import UserForm
from django.shortcuts import redirect
from .models import menu


def post(request):
        
        if request.method == "POST":
                form = UserForm(request.POST)
                if form.is_valid():
		    latest_menu_list = menu.objects.order_by('-id')[:1000]
                    post = form.save(commit=False)
                    post.save()
		    context ={'latest_menu_list': latest_menu_list,}
                    return render(request, "menu/index.html",context)
        else:
                form = UserForm()
                
        return render(request, 'menu/update.html', {'form': form})
        
    
        
def post_delete(request, menu_id):
        instance=get_object_or_404(menu, pk=menu_id)
        instance.deleted()
        messages.success(request, "succesfully deleted")
        #return redirect('detail',pk=post.pk)


#    response = "You're looking at the results of question %s."
#    return HttpResponse(response % menu_id)
