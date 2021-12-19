from django.shortcuts import render
from django.views.generic import View, TemplateView
from .forms import CategoryForm
from inventory.models import Stock, StockQuantity
from transactions.models import TableSaleBill, PurchaseBill


class HomeView(View):
    template_name = "home.html"
    def get(self, request):
        form = CategoryForm()        
        labels = []
        data = {}        
        stockqueryset = StockQuantity.objects.all().order_by('-measure_unit__quantity',)
        quantities = []
        labels =  []
        for item in stockqueryset:
            data.setdefault(item.stock.category, {})
            data[item.stock.category].setdefault('labels', [])
            data[item.stock.category].setdefault('quantity', [])
            data[item.stock.category]['quantity'].append(item.measure_unit.quantity)
            data[item.stock.category]['labels'].append(item.stock.name)
            quantities.append(item.measure_unit.quantity)
            labels.append(item.stock.name)
        sales = TableSaleBill.objects.order_by('-time')[:3]
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        context = {
            'labels'    : labels,
            'quantities' : quantities,
            'data'      : data,
            'sales'     : sales,
            'purchases' : purchases,
            'form': form
        }
        return render(request, self.template_name, context)

class AboutView(TemplateView):
    template_name = "about.html"