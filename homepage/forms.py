from django import forms

class CategoryForm(forms.Form):
    
    category = forms.MultipleChoiceField(label=('Categorias'),choices=[('C', 'Cocina'), ('B', 'Barra')], widget=forms.Select(attrs={'class': 'custom-select','id':'selectCategory'}))

  