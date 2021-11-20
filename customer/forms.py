from django import forms
from django.forms.widgets import TextInput


from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name','phone')
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Name'}),
            'phone': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Phone'}),
        }

