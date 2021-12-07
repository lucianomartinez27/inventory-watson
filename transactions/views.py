from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
    PurchaseBill,
    Supplier,
    PurchaseItem,
    Table,
    TableSaleBill,
    SaleItem,
)
from .forms import (
    SelectSupplierForm,
    PurchaseItemFormset,
    SupplierForm,
    SaleForm,
    SaleItemFormset,
)
from inventory.models import Stock


# shows a lists of all suppliers
class SupplierListView(ListView):
    model = Supplier
    template_name = "suppliers/suppliers_list.html"
    queryset = Supplier.objects.filter(is_deleted=False)
    paginate_by = 10


# used to add a new supplier
class SupplierCreateView(SuccessMessageMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/transacciones/proveedores'
    success_message = "Proveedor creado correctamente"
    template_name = "suppliers/edit_supplier.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Nuevo proveedor'
        context["savebtn"] = 'Agregar provedor'
        return context


# used to update a supplier's info
class SupplierUpdateView(SuccessMessageMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/transacciones/proveedores'
    success_message = "Detalles del provedor actualizados correctamente"
    template_name = "suppliers/edit_supplier.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Editar Proveedor'
        context["savebtn"] = 'Guardar cambios'
        context["delbtn"] = 'Eliminar Proovedor'
        return context


# used to delete a supplier
class SupplierDeleteView(View):
    template_name = "suppliers/delete_supplier.html"
    success_message = "Proovedor eliminado correctamente"

    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        return render(request, self.template_name, {'object': supplier})

    def post(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.is_deleted = True
        supplier.save()
        messages.success(request, self.success_message)
        return redirect('suppliers-list')


# used to view a supplier's profile
class SupplierView(View):
    def get(self, request, name):
        supplierobj = get_object_or_404(Supplier, name=name)
        bill_list = PurchaseBill.objects.filter(supplier=supplierobj)
        page = request.GET.get('page', 1)
        paginator = Paginator(bill_list, 10)
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)
        context = {
            'supplier': supplierobj,
            'bills': bills
        }
        return render(request, 'suppliers/supplier.html', context)


# shows the list of bills of all purchases
class PurchaseView(ListView):
    model = PurchaseBill
    template_name = "purchases/purchases_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


# used to select the supplier
class SelectSupplierView(View):
    form_class = SelectSupplierForm
    template_name = 'purchases/select_supplier.html'

    def get(self, request, *args, **kwargs):                                    # loads the form page
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    # gets selected supplier and redirects to 'PurchaseCreateView' class
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            supplierid = request.POST.get("supplier")
            supplier = get_object_or_404(Supplier, id=supplierid)
            return redirect('new-purchase', supplier.pk)
        return render(request, self.template_name, {'form': form})


# used to generate a bill object and save items
class PurchaseCreateView(View):
    template_name = 'purchases/new_purchase.html'

    def get(self, request, pk):
        # renders an empty formset
        formset = PurchaseItemFormset(request.GET or None)
        # gets the supplier object
        supplierobj = get_object_or_404(Supplier, pk=pk)
        context = {
            'formset': formset,
            'supplier': supplierobj,
        }                                                                       # sends the supplier and formset as context
        return render(request, self.template_name, context)

    def post(self, request, pk):
        # recieves a post method for the formset
        formset = PurchaseItemFormset(request.POST)
        # gets the supplier object
        supplierobj = get_object_or_404(Supplier, pk=pk)
        if formset.is_valid():
            # saves bill
            # a new object of class 'PurchaseBill' is created with supplier field set to 'supplierobj'
            billobj = PurchaseBill(supplier=supplierobj, buyer=request.user)
            # saves object into the db
            billobj.save()

            # for loop to save each individual form as its own object
            for form in formset:
                # false saves the item and links bill to the item
                billitem = form.save(commit=False)
                # links the bill object to the items
                billitem.billno = billobj
                # gets the stock item
                stock = get_object_or_404(
                    Stock, name=billitem.stock.name)       # gets the item
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                # updates quantity in stock db
                stock.quantity += billitem.quantity                              # updates quantity
                # saves bill item and stock
                stock.save()
                billitem.save()
            messages.success(
                request, "Compra de productos registrada correctamente")
            return redirect('inventory')
        formset = PurchaseItemFormset(request.GET or None)
        context = {
            'formset': formset,
            'supplier': supplierobj
        }
        return render(request, self.template_name, context)


# used to delete a bill object
class PurchaseDeleteView(SuccessMessageMixin, DeleteView):
    model = PurchaseBill
    template_name = "purchases/delete_purchase.html"
    success_url = '/transacciones/compras'

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = PurchaseItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity -= item.quantity
                stock.save()
        messages.success(
            self.request, "Detalle de compra eliminada correctamente")
        return super(PurchaseDeleteView, self).delete(*args, **kwargs)


# shows the list of bills of all sales
class SaleView(ListView):
    model = TableSaleBill
    queryset = TableSaleBill.objects.filter(closed=True)
    template_name = "sales/sales_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


class OpenTablesSaleView(ListView):
    model = TableSaleBill
    queryset = TableSaleBill.objects.filter(closed=False)
    template_name = "sales/tables_list.html"
    context_object_name = 'tables'
    ordering = ['-time']
    paginate_by = 10

# used to generate a bill object and save items


class SaleCreateView(View):
    template_name = 'sales/new_sale.html'

    def get(self, request):

        form = SaleForm(request.GET or None)
        # renders an empty formset
        formset = SaleItemFormset(request.GET or None)
        stocks = Stock.objects.filter(is_deleted=False)
        context = {
            'form': form,
            'formset': formset,
            'stocks': stocks,
            'title': 'Nueva venta'
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = SaleForm(request.POST)
        # recieves a post method for the formset
        formset = SaleItemFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            # saves bill
            billobj = form.save(commit=False)
            billobj.save()
            table = Table.objects.get(number=request.POST['table'])
            table.is_free = False
            table.save()
            # for loop to save each individual form as its own object
            for sold_item in formset:
               
               
                # false saves the item and links bill to the item
                billitem = sold_item.save(commit=False)
                # links the bill object to the items
                billitem.billno = billobj
                # gets the stock item
                stock = get_object_or_404(Stock, name=billitem.stock.name)
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                # updates quantity in stock db
                stock.quantity -= billitem.quantity
                # saves bill item and stock
                stock.save()
                billitem.save()
            messages.success(
                request, "Mesa iniciada correctamente")
            return redirect('open-tables')
        sold_item = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)
        context = {
            'form': form,
            'formset': formset,
            'stocks': Stock.objects.filter(is_deleted=False)
        }
        return render(request, self.template_name, context)


class SaleUpdateView(SuccessMessageMixin, View):
    template_name = 'sales/new_sale.html'

    def get(self, request, pk):

        form = SaleForm(request.GET or None, initial={
                        'waiter' : Table.objects.get(number=pk).waiter, 'table': Table.objects.filter(number=pk)})

        formset = SaleItemFormset(initial=[{'stock': product.stock, 'perprice': product.stock.sell_price,
                                            'quantity': product.quantity} for product in self.get_items_for_sale(pk)])
        form.fields['table'].choices = [
            (table.pk, str(table)) for table in Table.objects.filter(number=pk)]
        form.fields['table'].readonly = True

        context = {
            'form': form,
            'formset': formset,
            'stocks': self.get_total_stock(pk),
            'title': 'Editar venta'
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        # recieves a post method for the formset
        formset = SaleItemFormset(request.POST)
        
        self.restore_stock(pk)
        for sold_item in formset:
            # for loop to save each individual form as its own object
            if sold_item.is_valid():
                # false saves the item and links bill to the item
                billitem = sold_item.save(commit=False)
                # links the bill object to the items
                billitem.billno = TableSaleBill.objects.get(table=Table.objects.get(
                    pk=pk), closed=False)
                # gets the stock item
                stock = get_object_or_404(Stock, name=billitem.stock.name)
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                # updates quantity in stock db
                stock.quantity -= billitem.quantity
                # saves bill item and stock
                stock.save()
                billitem.save()
        messages.success(
            request, "Mesa actualizada correctamente")
        
        return redirect('open-tables')

    def restore_stock(self, pk):
        items_for_sale = self.get_items_for_sale(pk)
        for item in items_for_sale:
            stock = get_object_or_404(Stock, name=item.stock.name)
            stock.quantity += item.quantity
            stock.save()
        items_for_sale.delete()
        

    def get_items_for_sale(self, pk):
        return SaleItem.objects.filter(
            billno=TableSaleBill.objects.filter(
                table=Table.objects.get(
                    number=pk)
            ).get(closed=False))

    def get_total_stock(self, pk): # get total quantity of stock to update sales
        items_for_sale = self.get_items_for_sale(pk)
        queryset = [stock for stock in Stock.objects.all()]
        for item in items_for_sale:
            stock = next(filter(lambda stock: stock.name == item.stock.name, queryset )) # get the first item that matches condition
            stock.quantity += item.quantity
        return queryset


class SaleDeleteView(SuccessMessageMixin, DeleteView):
    model = TableSaleBill
    template_name = "sales/delete_sale.html"
    success_url = '/transacciones/ventas'

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.table.is_free = True
        self.object.table.save()
        self.object.closed = True
        self.object.save()
        messages.success(
            self.request, "Detalle de venta eliminada correctamente")
        return redirect('/transacciones/ventas')
