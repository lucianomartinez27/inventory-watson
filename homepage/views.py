from django.shortcuts import render
from django.views.generic import View, TemplateView
from .forms import CategoryForm
from inventory.models import Ingredient, Stock
from transactions.models import TableSaleBill, PurchaseBill


class HomeView(View):
    template_name = "home.html"
    def get(self, request):
        form = CategoryForm()        
        labels = []
        data = {}        
        stockqueryset = Ingredient.objects.order_by('-quantity',)
        quantities = []
        labels =  []
        for item in stockqueryset:
            data.setdefault(item.category, {})
            data[item.category].setdefault('labels', [])
            data[item.category].setdefault('quantity', [])
            data[item.category]['quantity'].append(item.quantity)
            data[item.category]['labels'].append(item.name)
            quantities.append(item.quantity)
            labels.append(item.name)
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