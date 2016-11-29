from django import forms
from .models import menu
from .models import specialmenu

class UserForm(forms.ModelForm):
    class Meta:
        model = menu
        fields = ['Name', 'Description','Nutrition', 'Price']
class specialUserForm(forms.ModelForm):
    class Meta:
        model = specialmenu
        fields = ['Name', 'Description','Nutrition', 'Price']