from django import forms
from django.forms.widgets import TextInput,NumberInput,Select,DateInput


from .models import Product,Quotation,QuotationItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','qty','price')
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Name'}),
            'price': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Price'}),
            'qty': NumberInput(attrs={'class': 'required form-control', 'placeholder': 'Quantity'}),
        }



class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ('customer','date','discount')
        widgets = {
            'customer': Select(attrs={'class': 'required form-control'}),
            'date': DateInput(attrs={'class': 'required form-control', 'placeholder': 'Date of Birth', 'id': 'Date', 'name': 'date', 'type': 'date'}),
            'discount': TextInput(attrs={'class': 'form-control', 'placeholder': 'Discount Amount'}),
        }

class QuotationItemForm(forms.ModelForm):
    class Meta:
        model = QuotationItem
        fields = ('product','qty')
        widgets = {
            'product': Select(attrs={'class': 'required form-control'}),
            'qty': NumberInput(attrs={'class': 'required form-control', 'placeholder': 'Quantity'}),
        }