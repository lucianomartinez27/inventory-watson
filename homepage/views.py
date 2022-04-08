from django.shortcuts import render
from django.views.generic import View, TemplateView
from .forms import CategoryForm
from inventory.models import StockQuantity
from transactions.models import TableSaleBill, PurchaseBill


class HomeView(View):
    template_name = "home.html"

    def get(self, request):
        form = CategoryForm()
        labels = []
        data = {}
        stockqueryset = StockQuantity.objects.all().order_by('-quantity__quantity', )
        quantities = []
        labels = []
        for item in stockqueryset:
            data.setdefault(item.stock.category, {})
            data[item.stock.category].setdefault('labels', [])
            data[item.stock.category].setdefault('quantity', [])
            data[item.stock.category]['quantity'].append(item.quantity.convert_to_max_unit().number())
            data[item.stock.category]['labels'].append(
                item.stock.name + " " + str(item.quantity.convert_to_max_unit().unit()))
            quantities.append(item.quantity.convert_to_max_unit().number())
            labels.append(item.stock.name + " " + str(item.quantity.convert_to_max_unit().unit()))
        sales = TableSaleBill.objects.order_by('-time')[:3]
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        context = {
            'labels': labels,
            'quantities': quantities,
            'data': data,
            'sales': sales,
            'purchases': purchases,
            'form': form
        }
        return render(request, self.template_name, context)


class AboutView(TemplateView):
    template_name = "about.html"
