from django import forms

from .models import Order

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
	