from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View,
    CreateView, 
    UpdateView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView
from .models import IngredientQuantity, Stock, StockQuantity, Table, Waiter
from .forms import  IngredientQuantityItemFormset, StockQuantityItemForm, StockForm, TableForm, WaiterForm
from django_filters.views import FilterView
from .filters import StockFilter




class StockListView(FilterView):
    model = Stock
    filterset_class = StockFilter
    template_name = 'inventory.html'
    paginate_by = 10
    ordering = ['name']

    def get_queryset(self):
        return Stock.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cocina"] = Stock.objects.filter(category='C')
        context["barra"] = Stock.objects.filter(category='B')
        return context
    

class StockCreateView(SuccessMessageMixin, CreateView):                                 # createview class to add new stock, mixin used to display message
    model = Stock                            # setting 'StockForm' form as form
    template_name = "edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = '/inventario'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Producto creado correctamente"                             # displays message when form is submitted
                          

    def get(self, request):
        form = StockForm(request.GET or None)
        formset = IngredientQuantityItemFormset(request.GET or None)
        quantity_formset = StockQuantityItemForm()
                                                     
        
        context = {
            'form'      : form,
            'formset'   : formset,
            'quantity_formset': quantity_formset,
            'title'    : "Nuevo producto",
            'savebtn' : 'Agregar al inventario',
        }

        return render(request, self.template_name, context)       

    def post(self, request):
        form = StockForm(request.POST)
        stock_quantity_form = StockQuantityItemForm(request.POST)
        formset = IngredientQuantityItemFormset(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.save()
            for ingredient_form in formset:
                if ingredient_form.is_valid() and ingredient_form.cleaned_data:
                    print(ingredient_form.cleaned_data)
                    ingredient = IngredientQuantity(stock=stock,
                    ingredient=ingredient_form.cleaned_data['ingredient'],
                    quantity=ingredient_form.cleaned_data['quantity'])
                    ingredient.save()
                 
            
            if stock_quantity_form.is_valid() and not stock_quantity_form.cleaned_data['is_manufactured']:
               quantity = StockQuantity(stock= stock, quantity= stock_quantity_form.cleaned_data['quantity'])
               quantity.save()

            messages.success(request, "Producto agregado correctamente")
            return redirect('inventory')

        form = StockForm(request.GET or None)
        formset = IngredientQuantityItemFormset(request.GET or None)
        context = {
            'form'      : form,
            'formset'   : formset,
            'title'    : "Nuevo producto",
            'savebtn' : 'Agregar al inventario',
        }
        return render(request, self.template_name, context)

class StockUpdateView(SuccessMessageMixin, UpdateView):                                 # updateview class to edit stock, mixin used to display message
    template_name = "edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = '/inventario'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Producto actualizado correctamente"                             # displays message when form is submitted

    def get(self, request, pk):                                               # used to send additional context
        context = {}
        context['object'] = Stock.objects.get(id=pk)
        form = StockForm(instance=context['object'])

        
        context['form'] = form
        context["title"] = 'Editar producto'
        context["savebtn"] = 'Actualizar producto'
        context["delbtn"] = 'Vender producto'
        ingredients = IngredientQuantity.objects.filter(stock=context['object'])
        context["formset"] = IngredientQuantityItemFormset(initial=[{'ingredient': ingredient.ingredient, 'quantity': ingredient.quantity} for ingredient in ingredients])
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        stock = Stock.objects.get(id=pk)
        form = StockForm(request.POST or None, instance =stock )
        IngredientQuantity.objects.filter(stock=stock).delete()

        formset = IngredientQuantityItemFormset(request.POST)
        if form.is_valid():
            form.save()
            for ingredient_form in formset:
                if ingredient_form.is_valid():
                    ingredient = IngredientQuantity(stock=stock,
                        ingredient=ingredient_form.cleaned_data['ingredient'],
                        quantity=ingredient_form.cleaned_data['quantity'])
                    ingredient.save()
            messages.success(request, self.success_message)
        return redirect('inventory')
    


class StockDeleteView(View):
    template_name = "delete_item.html"
    success_message = "Producto eliminado correctamente"
    
    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return render(request, self.template_name, {'object' : stock,'cancel_url': 'inventory'})

    def post(self, request, pk):  
        stock = get_object_or_404(Stock, pk=pk)
        stock.delete()                                              
        messages.success(request, self.success_message)
        return redirect('inventory')


class TableCreateView(SuccessMessageMixin, CreateView):
    model = Table
    form_class = TableForm
    success_url = '/inventario/mesas-y-mozos'
    success_message = "Mesa creada correctamente"
    template_name = "edit_table.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Nueva mesa'
        context["savebtn"] = 'Agregar mesa'
        return context


class WaiterCreateView(SuccessMessageMixin, CreateView):
    model = Waiter
    form_class = WaiterForm
    success_url = '/tables-and-waiters'
    success_message = "Mozo creado correctamente"
    template_name = "edit_waiter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Nuevo mozo'
        context["savebtn"] = 'Agregar mozo'
        return context


class TablesAndWaitersView(TemplateView):
    template_name = "tables-and-waiters.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables'] = Table.objects.all()
        context['waiters'] = Waiter.objects.all()
        return context

class TableDeleteView(SuccessMessageMixin, DeleteView):
    model = Table
    template_name = "delete_item.html"
    success_url = '/inventario/mesas-y-mozos'
    success_message = 'Mesa eliminada correctamente'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["cancel_url"] = 'tables-and-waiters'
            return context

class TableUpdateView(SuccessMessageMixin, UpdateView):
    model = Table
    template_name = "edit_table.html"
    success_url = '/inventario/mesas-y-mozos'
    success_message = 'Mesa actualizada correctamente'
    form_class = TableForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Editar Mesa'
        context["savebtn"] = 'Guardar cambios'
        return context
     

class WaiterDeleteView(SuccessMessageMixin, DeleteView):
    model = Waiter
    template_name = "delete_item.html"
    success_url = '/inventario/mesas-y-mozos'
    success_message = 'Mozo eliminado correctamente'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["cancel_url"] = 'tables-and-waiters'

            return context



class WaiterUpdateView(SuccessMessageMixin, UpdateView):
    model = Waiter
    template_name = "edit_waiter.html"
    success_url = '/inventario/mesas-y-mozos'
    success_message = 'Mozo actualizado correctamente'
    form_class = WaiterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Editar Mozo'
        context["savebtn"] = 'Guardar cambios'
        return context

def get_verbose_name(object): 
    return object._meta.verbose_name