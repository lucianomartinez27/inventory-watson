from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View,
    CreateView, 
    UpdateView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Category, IngredientQuantity, Stock
from .forms import CategoryForm, IngredientQuantityItemFormset, StockForm
from django_filters.views import FilterView
from .filters import StockFilter


class StockListView(FilterView):
    model = Stock
    filterset_class = StockFilter
    template_name = 'inventory.html'
    paginate_by = 10
    ordering = ['-quantity']

    
class CategoryDeleteView(View):                                                            # view class to delete stock
    template_name = "delete_category.html"                                                 # 'delete_stock.html' used as the template
    success_message = "Categoria eliminada correctamente"                             # displays message when form is submitted
    
    def get(self, request, pk):
        stock = get_object_or_404(Category, pk=pk)
        return render(request, self.template_name, {'object' : stock})

    def post(self, request, pk):  
        stock = get_object_or_404(Category, pk=pk)
        stock.delete()                                              
        messages.success(request, self.success_message)
        return redirect('inventory')
        

        return context    

class CategoryCreateView(SuccessMessageMixin, CreateView):                                
    model = Stock                                                                       
    form_class = CategoryForm                                                              
    template_name = "add_category.html"                                                  
    success_url = '/inventario/agregar-categoria'                                                         
    success_message = "Categoria creada correctamente"                            

    def get_context_data(self, **kwargs):                                              
        context = super().get_context_data(**kwargs)
        context["title"] = 'Nueva categoria'
        context["savebtn"] = 'Agregar categoria'
        context['categories'] = Category.objects.all()
        

        return context    

class StockCreateView(SuccessMessageMixin, CreateView):                                 # createview class to add new stock, mixin used to display message
    model = Stock                            # setting 'StockForm' form as form
    template_name = "edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = '/inventario'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Producto creado correctamente"                             # displays message when form is submitted
                          

    def get(self, request):
        form = StockForm(request.GET or None)
        formset = IngredientQuantityItemFormset(request.GET or None)                                                 # used to send additional context
        
        context = {
            'form'      : form,
            'formset'   : formset,
            'title'    : "Nuevo producto",
            'savebtn' : 'Agregar al inventario',
        }

        return render(request, self.template_name, context)       

    def post(self, request):
        form = StockForm(request.POST)
        
        formset = IngredientQuantityItemFormset(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.save()
            if formset.is_valid():
                for form in formset:
                    print(form.cleaned_data)
                    # false saves the item and links bill to the item
                    ingredient = IngredientQuantity(stock=stock,
                    ingredient=form.cleaned_data['ingredient'],
                    quantity=form.cleaned_data['quantity'])
                    ingredient.save()
            messages.success(request, "Producto agregado correctamente")
            return redirect('inventory')

        form = StockForm(request.GET or None)
        formset = IngredientQuantityItemFormset(request.GET or None)
        context = {
            'form'      : form,
            'formset'   : formset,
        }
        return render(request, self.template_name, context)

    

class StockUpdateView(SuccessMessageMixin, UpdateView):                                 # updateview class to edit stock, mixin used to display message
    model = Stock                                                                       # setting 'Stock' model as model
    form_class = StockForm                                                              # setting 'StockForm' form as form
    template_name = "edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = '/inventario'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Producto actualizado correctamente"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Editar producto'
        context["savebtn"] = 'Actualizar producto'
        context["delbtn"] = 'Vender producto'
        context["formset"] = IngredientQuantityItemFormset()
        return context


class StockDeleteView(View):                                                            # view class to delete stock
    template_name = "delete_stock.html"                                                 # 'delete_stock.html' used as the template
    success_message = "Producto eliminado correctamente"                             # displays message when form is submitted
    
    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return render(request, self.template_name, {'object' : stock})

    def post(self, request, pk):  
        stock = get_object_or_404(Stock, pk=pk)
        stock.delete()                                              
        messages.success(request, self.success_message)
        return redirect('inventory')