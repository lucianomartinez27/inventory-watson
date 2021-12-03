from django.contrib import admin
from .models import Stock, Category, IngredientQuantity

admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(IngredientQuantity)
