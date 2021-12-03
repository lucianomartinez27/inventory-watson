from django.db import models
    


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True,error_messages={'unique': u'La categoria ya existe en el inventario'})

    def __str__(self):
	    return self.name

    class Meta:
        verbose_name_plural = "categories"





class IngredientQuantity(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE)
    ingredient = models.ForeignKey("Stock", on_delete=models.CASCADE, null=True, related_name="ingredient")
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return self.ingredient.name + " para " + self.stock.name

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True,error_messages={'unique': u'El producto ya existe en el inventario'})
    quantity = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  null=True)
    buy_price = models.FloatField(default=0)
    sell_price = models.FloatField(default=0)

    def get_ingredients(self):
        return IngredientQuantity.objects.filter(stock=self)

    def get_total_cost(self):
        total = self.buy_price
        for quantity in self.get_ingredients():
            total += quantity.ingredient.get_total_cost() * quantity.quantity
        return total

    class Meta:
        ordering = ['quantity']
  
    def __str__(self):
	    return self.name



    



