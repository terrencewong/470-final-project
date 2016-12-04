from django import forms
from .models import Order, Alert, OrderedMenuItems
from django.contrib.admin import widgets
from menu.models import menu

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
		model = menu
		fields = ('Name', 'Description', 'Nutrition', 'Price')

	Name = forms.CharField(label="Name", required=True)
	Description = forms.CharField(label="Description")
	Nutrition = forms.CharField(label="Nutrition")
	Price = forms.IntegerField(label="Price")

class ItemForm(forms.ModelForm):

    class Meta:
        model = OrderedMenuItems
        fields = ('num_items', 'notes')
        exclude = ('order_id', 'item_name')

    #order_id = forms.ModelChoiceField(queryset=Order.objects.all() , label="Code", required=True)#, readonly:True)#, disabled=True)
    #item_name = forms.ModelChoiceField(queryset=menu.objects.all(), label="Menu Item")#, required=True)
    num_items = forms.IntegerField(min_value=0, initial=0, label = "Number of items", required=False)
    notes = forms.CharField(label="Notes", required=False, widget=forms.Textarea)

class OrderStartForm(forms.Form):
    Code = forms.CharField(label = 'Code', max_length=10, required=True)
    Table = forms.IntegerField(min_value=1, initial=1, label = 'Table', required=True)

class KitchenForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('Status',)

class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())

class ContactServerForm(forms.ModelForm):
	class Meta:
		model = Alert
		fields = ('Message',)
		exclude = ('Order', 'Resolved',)
	Message = forms.CharField(label="Message", required=False, widget=forms.Textarea)

class AlertForm(forms.Form):
    Order = forms.IntegerField(label = 'Order', required=True)
    Message = forms.CharField(label = 'Message')
    Resolved = forms.BooleanField(label = 'Resolved')
