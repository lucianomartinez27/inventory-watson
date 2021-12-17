from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from .models import  IngredientQuantity, MeasureUnit, Stock, StockQuantity, Table, Waiter




class StockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['category'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['category'].label = 'Categoria'
        self.fields['name'].label = 'Nombre'
        self.fields['buy_price'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})
        self.fields['buy_price'].label = 'Precio compra'
        self.fields['sell_price'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})
        self.fields['sell_price'].label = 'Precio venta'
        self.fields['is_for_sale'].label = 'Para venta al público'

    class Meta:
        model = Stock
        fields = ['name', 'category', 'buy_price', 'is_for_sale', 'sell_price']



class WaiterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['name'].label = 'Nombre'


    class Meta:
        model = Waiter
        fields = ['name']

class IngredientQuantityItemForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField( label=('Stock'),queryset=Stock.objects.all(),blank=False,
    widget=forms.Select(attrs={'class': 'custom-select','id':'selectCategory'}))
    quantity = forms.IntegerField(min_value=1)
    quantity.widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '1', })

    class Meta:
        model = IngredientQuantity
        fields = ['quantity', 'ingredient']
    
class StockQuantityItemForm(forms.Form):
    quantity = forms.IntegerField(required=False)
    is_manufactured = forms.BooleanField(label=('Es producción propia: '), required=False)
    quantity.widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '1', })

class MeasureUnitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit'].widget.attrs.update({'class': 'custom-select'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0',})
    class Meta:
        model = MeasureUnit
        fields = ['unit', 'quantity']


class TableForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['number'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only'})
        
    class Meta:
        model = Table
        fields = ['number']



# formset used to render multiple 'SaleItemForm'
IngredientQuantityItemFormset = formset_factory(IngredientQuantityItemForm, extra=1)
MeasureUnitItemFormset = formset_factory(MeasureUnitForm, extra=1)
