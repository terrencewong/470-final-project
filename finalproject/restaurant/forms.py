from django import forms
from .models import Order, OrderedMenuItems
from django.contrib.admin import widgets

class TableIDForm(forms.ModelForm):
	
	class Meta:	
		model = Order
		fields = ('Code',)

	#code_id = forms.CharField(label = 'Code ID', max_length = 64)
	
	widgets = {
		#'tableID': forms.TextInput(
			#attrs={'placeholder': 'TableID', 'class':'form-control'}
		#),
		'code_id': forms.TextInput(
			attrs={'placeholder': 'code_id', 'class':'form-control'}
		),
		
	}

class OrderForm(forms.ModelForm):

	class Meta:
		model = OrderedMenuItems
		fields = ('order_id', 'item_name',)#, 'table_id', 'item_name', 'num_items', 'notes',)
	
	#order_id = models.Order(Code)
	order_id = forms.CharField(label="Code", required=True)#, readonly:True)#, disabled=True)
	item_name = forms.CharField(label="Menu Item")#, required=True)
	num_items = forms.IntegerField(min_value=0, initial=0, label = 'Number of items', required=False)
	notes = forms.CharField(label="Notes", required=False, widget=forms.Textarea)

	
class OrderStartForm(forms.Form):
    Code = forms.CharField(label = 'Code', max_length=10, required=True)
    Table = forms.IntegerField(label = 'Table', required=True)

class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())

