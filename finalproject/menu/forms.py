from django import forms
from .models import menu

class UserForm(forms.ModelForm):
    class Meta:
        model = menu
        fields = ['Name', 'Description','Nutrition', 'Price']