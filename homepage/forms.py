from django import forms
from inventory.models import Category



class CategoryForm(forms.Form):
    
    category = forms.MultipleChoiceField(label=('Categorias'),choices=[('C', 'Cocina'), ('B', 'Barra')], widget=forms.Select(attrs={'class': 'custom-select','id':'selectCategory'}))

  