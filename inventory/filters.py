import django_filters
from .models import Stock    
from django_filters.filters import OrderingFilter

class StockFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    o = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('quantity', 'o'),
        ), widget=django_filters.widgets.LinkWidget
    )
    
    class Meta:
        model = Stock
        fields = ['name', 'o', 'category']

