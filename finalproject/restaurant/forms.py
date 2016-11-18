from django import forms
from .models import Order
from django.contrib.admin import widgets

class OrderStartForm(forms.Form):
    Code = forms.CharField(label = 'Code', max_length=10, required=True)
    Table = forms.IntegerField(label = 'Table', required=True)

class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())
