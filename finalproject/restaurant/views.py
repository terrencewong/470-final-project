from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from .forms import TableIDForm
from .models import Table, Order, MenuItem
from django.http import HttpResponseRedirect


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
		
			try:
				p = Order.objects.get(Code=code_id)
				
				#order = form.save(commit=False)
				#order.save()
				
				#reverse_url = reverse('OrderNow', args=[code_id])				
				#return HttpResponseRedirect(reverse_url)
				
				return HttpResponse("This exists.")
				
			except Order.DoesNotExist:
			
				return HttpResponse("This DOESNT exists.")				
	
	else:
		form = TableIDForm()		
		
	if request.GET.get('table', ''):
		
		table = Table.objects.get(id=request.GET.get('table', ''))	
	
	variables = {
		'form': form,
	}
	
	template = 'restaurant/TableIDVerificationForm.html'
	
	return render(request, template, variables)	
	
	
def ordernow(request, code):
	
	#contact = Contact.objects.get(code=contact_id)
	#form = TableIDForm(request.POST)
	#code = form.data['Code']
	
	#menu_items = MenuItem.objects.all()
	#output = ', '.join([q.Name for q in menu_items])
	#return HttpResponse(output)
	
	menu_items = MenuItem.objects.all()
	context = {'menu_items': menu_items}
	return render(request, 'restaurant/order-now.html', context)
	#code = Oder.objects.get(pk=Code)
	#return render(request, 'restaurant/order-now.html')
	#return HttpResponse("Welcome to the Order Form.")
