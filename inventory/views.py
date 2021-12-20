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

from transactions.models import PurchaseBill, PurchaseItem
from .models import IngredientQuantity, Stock, StockQuantity, Table, Waiter
from .forms import IngredientQuantityItemFormset, MeasureUnitItemFormset, StockQuantityItemForm, StockForm, TableForm, WaiterForm, MeasureUnitForm
from django_filters.views import FilterView
from .filters import StockFilter


class StockListView(FilterView):
    model = Stock
    filterset_class = StockFilter
    template_name = 'inventory.html'
    paginate_by = 10
    ordering = ['name']

    def get_queryset(self):
        return Stock.objects.all().exclude(stockquantity=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = {'Cocina': context["filter"]._qs.filter(
            category='C'), 'Barra': context["filter"]._qs.filter(category='B')}

        return context


class ManufacturedListView(FilterView):
    model = Stock
    filterset_class = StockFilter
    template_name = 'inventory.html'
    paginate_by = 10
    ordering = ['name']

    def get_queryset(self):
        return Stock.objects.filter(stockquantity=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = {'Cocina': context["filter"]._qs.filter(
            category='C'), 'Barra': context["filter"]._qs.filter(category='B')}

        return context


# createview class to add new stock, mixin used to display message
class StockCreateView(SuccessMessageMixin, CreateView):
    model = Stock                            # setting 'StockForm' form as form
    # 'edit_stock.html' used as the template
    template_name = "edit_stock.html"
    # redirects to 'inventory' page in the url after submitting the form
    success_url = '/inventario'
    # displays message when form is submitted
    success_message = "Producto creado correctamente"

    def get(self, request):
        form = StockForm(request.GET or None)
        formset = IngredientQuantityItemFormset(
            request.GET or None, prefix='ingredient-form')
        measure_formset = MeasureUnitItemFormset(
            request.GET or None, prefix='ingredient-measure')
        quantity_formset = StockQuantityItemForm()
        formsets = zip(formset, measure_formset)
        context = {
            'form': form,
            'formset': formset,
            'formsets': formsets,
            'quantity_formset': quantity_formset,
            'stock_measure_form': MeasureUnitForm(request.GET or None),
            'measure_formset': measure_formset,
            'title': "Nuevo producto",
            'savebtn': 'Agregar al inventario',
            'stock_quantitys': [stock for stock in StockQuantity.objects.all()],
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = StockForm(request.POST)
        measure_form = MeasureUnitItemFormset(
            request.POST, prefix='ingredient-measure')
        stock_quantity_form = MeasureUnitForm(request.POST)
        formset = IngredientQuantityItemFormset(
            request.POST, prefix='ingredient-form')
        is_manufactured = StockQuantityItemForm(request.POST)

        if form.is_valid():

            stock = form.save()

            if stock_quantity_form.is_valid() and is_manufactured.is_valid() and not is_manufactured.cleaned_data['is_manufactured']:
                quantity_unit = stock_quantity_form.save()
                quantity = StockQuantity(stock=stock,
                                         quantity=quantity_unit)
                quantity.save()
                bill = PurchaseBill(buyer=request.user)
                bill.save()
                quantity_unit.pk = None
                quantity_unit.save()
                sale = PurchaseItem(billno=bill, stock=stock, quantity=quantity_unit,
                                    perprice=stock.buy_price, totalprice=stock.buy_price * quantity_unit.quantity)
                sale.save()
            else:
                for index, ingredient_form in enumerate(formset):
                    if ingredient_form.is_valid() and ingredient_form.cleaned_data and measure_form[index].is_valid():
                        measure = measure_form[index].save()
                        ingredient = IngredientQuantity(stock=stock,
                                                        ingredient=ingredient_form.cleaned_data['ingredient'],
                                                        quantity=measure)
                        ingredient.save()

            messages.success(request, "Producto agregado correctamente")
            return redirect('inventory')

        form = StockForm(request.GET or None)
        formset = IngredientQuantityItemFormset(request.GET or None)
        context = {
            'form': form,
            'formset': formset,
            'title': "Nuevo producto",
            'savebtn': 'Agregar al inventario',
        }
        return render(request, self.template_name, context)


# updateview class to edit stock, mixin used to display message
class StockUpdateView(SuccessMessageMixin, UpdateView):
    # 'edit_stock.html' used as the template
    template_name = "edit_stock.html"
    # redirects to 'inventory' page in the url after submitting the form
    success_url = '/inventario'
    # displays message when form is submitted
    success_message = "Producto actualizado correctamente"

    # used to send additional context
    def get(self, request, pk):

        this_instance = Stock.objects.get(id=pk)
        form = StockForm(instance=this_instance)

        ingredients = IngredientQuantity.objects.filter(stock=this_instance)
        formset = IngredientQuantityItemFormset(
            initial=[{'ingredient': ingredient.ingredient} for ingredient in ingredients], prefix='ingredient-form')
        measure_formset = MeasureUnitItemFormset(initial=[{'unit': ingredient.quantity.unit, 'quantity': ingredient.quantity.quantity, }
                                                          for ingredient in ingredients], prefix='ingredient-measure')

        formsets = zip(formset, measure_formset)
        context = {
            'object': this_instance,
            'form': form,
            'title': "Editar producto",
            'savebtn': 'Actualizar producto',
            'formset': formset,
            'measure_formset': measure_formset,
            'formsets': formsets,
            'quantity_formset': StockQuantityItemForm(),
            'stock_measure_form': MeasureUnitForm(request.GET or None),
            'stock_quantitys': [stock for stock in StockQuantity.objects.all()],
            'empty_stock_quantity': len(StockQuantity.objects.filter(stock=Stock.objects.get(id=pk))) == 0
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        stock = Stock.objects.get(id=pk)
        form = StockForm(request.POST or None, instance=stock)
        try:
            IngredientQuantity.objects.filter(stock=stock).delete()
            StockQuantity.objects.get(stock=stock).delete()
        except (StockQuantity.DoesNotExist, IngredientQuantity.DoesNotExist):
            pass
        finally:
            formset = IngredientQuantityItemFormset(
                request.POST, prefix='ingredient-form')
            measure_form = MeasureUnitItemFormset(
                request.POST, prefix='ingredient-measure')
            is_manufactured = StockQuantityItemForm(request.POST)
            stock_quantity = MeasureUnitForm(request.POST)
            if form.is_valid():
                form.save()
                
                if is_manufactured.is_valid() and not is_manufactured.cleaned_data['is_manufactured']:
                    quantity_unit = stock_quantity.save()
                    quantity = StockQuantity(
                        stock=stock, quantity=quantity_unit)
                    quantity.save()

                    
                    quantity_unit.pk = None
                    quantity_unit.save()
                    bill = PurchaseBill(buyer=request.user)
                    bill.save()
                    sale = PurchaseItem(billno=bill, stock=stock, quantity=quantity_unit,
                                        perprice=stock.buy_price, totalprice=stock.buy_price * quantity_unit.quantity)
                    sale.save()
                else:
                    print(len(formset))
                    print(len(measure_form))
                    for index, ingredient_form in enumerate(formset):
                        print(measure_form[index].is_valid())
                        print(ingredient_form.is_valid())
                        if ingredient_form.is_valid() and ingredient_form.cleaned_data and measure_form[index].is_valid():

                            measure = measure_form[index].save()
                            ingredient = IngredientQuantity(stock=stock,
                                                            ingredient=ingredient_form.cleaned_data['ingredient'],
                                                            quantity=measure)
                            ingredient.save()

                messages.success(request, self.success_message)
            return redirect('inventory')


class StockDeleteView(View):
    template_name = "delete_item.html"
    success_message = "Producto eliminado correctamente"

    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return render(request, self.template_name, {'object': stock, 'cancel_url': 'inventory', 'title': 'Eliminar Stock'})

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
    success_url = '/inventario/mesas-y-mozos'
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
        context["title"] = 'Eliminar mesa'
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
        context["title"] = 'Eliminar mozo'

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
