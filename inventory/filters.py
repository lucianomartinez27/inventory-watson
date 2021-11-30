import django_filters
from .models import Category, Stock    
from django_filters.filters import OrderingFilter

class StockFilter(django_filters.FilterSet):                            # Stockfilter used to filter based on name
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    o = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('quantity', 'o'),
        ), widget=django_filters.widgets.LinkWidget
    )
    
    class Meta:
        model = Stock
        fields = ['name', 'o', 'category']

