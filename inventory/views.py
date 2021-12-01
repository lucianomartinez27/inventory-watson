from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View,
    CreateView, 
    UpdateView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Category, Stock
from .forms import CategoryForm, StockForm
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
    model = Stock                                                                       # setting 'Stock' model as model
    form_class = StockForm                                                              # setting 'StockForm' form as form
    template_name = "edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = '/inventario'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Producto creado correctamente"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Nuevo producto'
        context["savebtn"] = 'Agregar al inventario'
        

        return context       


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