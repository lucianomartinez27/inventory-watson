from django import forms
from inventory.models import Category



class CategoryForm(forms.Form):
    
    category = forms.ModelChoiceField(label=('Categorias'),queryset=Category.objects.filter(stock__isnull=False).all(), widget=forms.Select(attrs={'class': 'custom-select','id':'selectCategory'}))

  