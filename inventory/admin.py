from django.contrib import admin
from .models import  Stock, IngredientQuantity, Table, Waiter

admin.site.register(Stock)
admin.site.register(IngredientQuantity)
admin.site.register(Table)
admin.site.register(Waiter)
