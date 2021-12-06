from django.contrib import admin
from .models import (
    Supplier, 
    PurchaseBill, 
    PurchaseItem,
    Table,
    TableSaleBill, 
    SaleItem,
    Waiter,
)
admin.site.register(Waiter)
admin.site.register(Supplier)
admin.site.register(PurchaseBill)
admin.site.register(PurchaseItem)
admin.site.register(TableSaleBill)
admin.site.register(SaleItem)
admin.site.register(Table)
