from django import forms
from .models import Order
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

class OrderStartForm(forms.Form):
    Code = forms.CharField(label = 'Code', max_length=10, required=True)
    Table = forms.IntegerField(label = 'Table', required=True)

class KitchenForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('Timestamp', 'Code', 'Table', 'StartTime')

class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())
