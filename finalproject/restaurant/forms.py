from django import forms
<<<<<<< HEAD
from .models import Order, Alert, OrderedMenuItems
from django.contrib.admin import widgets
from menu.models import menu
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
=======
from .models import Order
from django.contrib.admin import widgets
>>>>>>> caca943b08e3c9846d830490d7045b695ad02803

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

<<<<<<< HEAD
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
=======
class OrderStartForm(forms.Form):
    Code = forms.CharField(label = 'Code', max_length=10, required=True)
    Table = forms.IntegerField(label = 'Table', required=True)
>>>>>>> caca943b08e3c9846d830490d7045b695ad02803

class KitchenForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('Status',)

class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())
<<<<<<< HEAD

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

class CreateAccountForm(UserCreationForm):
	username = forms.CharField(required = True)
	first_name = forms.CharField(required = True)
	last_name = forms.CharField(required = True)
	email = forms.EmailField(required = True)
	
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
		
	def save(self, commit = True):
		user = super(CreateAccountForm, self).save(commit = False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		
		if commit:
			user.save()
			
		return user
=======
>>>>>>> caca943b08e3c9846d830490d7045b695ad02803
