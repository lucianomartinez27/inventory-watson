from django.contrib import admin
from .models import  MeasureUnit, Stock, IngredientQuantity, Table, Waiter, StockQuantity

admin.site.register(Stock)
admin.site.register(IngredientQuantity)
admin.site.register(Table)
admin.site.register(Waiter)
admin.site.register(StockQuantity)
admin.site.register(MeasureUnit)