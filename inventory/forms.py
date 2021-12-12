from django import forms
from django.forms.formsets import formset_factory
from .models import  IngredientQuantity, Stock, Table, Waiter




class StockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['category'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['category'].label = 'Categoria'
        self.fields['name'].label = 'Nombre'
        self.fields['sell_price'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})
        self.fields['sell_price'].label = 'Precio venta'

    class Meta:
        model = Stock
        fields = ['name', 'category', 'sell_price']



class WaiterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['name'].label = 'Nombre'


    class Meta:
        model = Waiter
        fields = ['name']

class IngredientQuantityItemForm(forms.Form):
    ingredient = forms.ModelChoiceField(label=('Stock'),queryset=Stock.objects.all(),
    widget=forms.Select(attrs={'class': 'custom-select','id':'selectCategory'}))
    quantity = forms.IntegerField()
    quantity.widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '1', 'required': 'true'})
    


class TableForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['number'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only'})
        
    class Meta:
        model = Table
        fields = ['number']



# formset used to render multiple 'SaleItemForm'
IngredientQuantityItemFormset = formset_factory(IngredientQuantityItemForm, extra=1)