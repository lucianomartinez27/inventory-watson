from django.db import models
from unum.units import *




class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True,error_messages={'unique': u'El producto ya existe en el inventario'})
    category = models.CharField(choices=[('C', 'Cocina'), ('B', 'Barra')],default='C', max_length=1)
    buy_price = models.FloatField(default=0)
    sell_price = models.FloatField(default=0)
    is_for_sale = models.BooleanField(default=False)

    def get_ingredients(self):
        return IngredientQuantity.objects.filter(stock=self)

    def get_total_cost(self):
        total = self.buy_price
        for ingredient_quantity in self.get_ingredients():
            total += ingredient_quantity.ingredient.get_total_cost() * ingredient_quantity.quantity
        return total
    
    def get_quantity(self):
        try:
            return StockQuantity.objects.get(stock=self).quantity
        except StockQuantity.DoesNotExist:
            return '-'
    
    def sell(self, quantity_sold):
        try:
            StockQuantity.objects.get(stock=self).sell(quantity_sold)
        except StockQuantity.DoesNotExist:
            pass
        for ingredient in IngredientQuantity.objects.filter(stock=self):
            ingredient.ingredient.sell(ingredient.quantity * quantity_sold)

    def buy(self, purchased_amount):
        try:
            StockQuantity.objects.get(stock=self).buy(purchased_amount)
        except StockQuantity.DoesNotExist:
            pass
        for ingredient in IngredientQuantity.objects.filter(stock=self):
            ingredient.ingredient.buy(ingredient.quantity * purchased_amount)

    class Meta:
        ordering = ['name']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
  
    def __str__(self):
	    return self.name

class MeasureUnit(models.Model):
    MEASURE_CHOICES = [
        ('kg','KILOGRAMOS'),
        ('g', 'GRAMOS'),
        ('cc', 'CENTIMETROS CUBICOS'),
        ('lt', 'LITROS')
    ]
    id = models.AutoField(primary_key=True)
    unit = models.CharField(max_length=2, choices=MEASURE_CHOICES, default='gr')
    quantity = models.PositiveIntegerField(default=0)


    def as_unit(self):
        units = {'g':g, 'kg':kg, 'cc':cm*cm*cm, 'lt': L}
        return self.quantity * units[self.unit]

    def substract_quantity_by_unit(self, another_unit):
        return self.as_unit() - another_unit.as_unit()

    def __str__(self):
        return str(self.quantity) + ' ' + self.unit

        
class StockQuantity(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.OneToOneField(Stock, on_delete = models.CASCADE, unique=True)
    quantity = models.PositiveIntegerField(default=0)
    measure_unit = models.ForeignKey(MeasureUnit, on_delete = models.CASCADE, null=True, blank=True)

    def sell(self, quantity_sold):
        self.quantity -= quantity_sold
        self.save()
    
    def buy(self, purchased_amount):
        self.quantity += purchased_amount
        self.save()


    def __str__(self):
        return str(self.quantity) + " " + str(self.stock)

class IngredientQuantity(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, related_name="ingredient")
    quantity = models.IntegerField(default=1)
    measure_unit = models.ForeignKey(MeasureUnit, on_delete = models.CASCADE, null=True, blank=True)

    
    def __str__(self):
        if (self.measure_unit):
            quantity = str(self.measure_unit.quantity) + " " + self.measure_unit.unit
        else:
            quantity = str(self.quantity)

        return quantity + " de " + self.ingredient.name + " para " + self.stock.name

    class Meta:
        unique_together = ('ingredient', 'stock',)
        verbose_name = 'Ingrediente para producto'
        verbose_name_plural = 'Ingredientes para producto'

class Waiter(models.Model):
    name = models.CharField('Nombre', max_length=15, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Mozo'
        verbose_name_plural = 'Mozos'

class Table(models.Model):
    number = models.IntegerField(primary_key=True,verbose_name='Numero')
    is_free = models.BooleanField(default=True)
    def __str__(self):
        return 'Mesa N°' + str(self.number)
    

    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'
        

