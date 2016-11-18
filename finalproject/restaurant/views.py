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
			request.session['Code'] = code_id
			
			try:
				p = Order.objects.get(Code=code_id)
				
				#order = form.save(commit=False)
				
				#order.save()
				
				#return redirect('order-now.html', code='code_id')
				
				#return render_to_response('order-now.html', {'code_id': code})
				
				reverse_url = reverse('OrderNow')				
				return HttpResponseRedirect(reverse_url)
				
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
	menu_item_list = MenuItem.objects.all()
	return render(request, 'restaurant/order-now.html', {'code':code, 'menu_item_list':menu_item_list})
