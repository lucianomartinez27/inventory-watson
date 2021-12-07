from django.contrib import admin
from .models import Stock, Category, IngredientQuantity, Table, Waiter

admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(IngredientQuantity)
admin.site.register(Table)
admin.site.register(Waiter)