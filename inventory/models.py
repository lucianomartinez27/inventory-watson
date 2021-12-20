from django.db import models
from django.apps import apps
from django.db.models.query_utils import Q

from unum.units import *
from unum import *
U = new_unit('U')


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True, error_messages={
                            'unique': u'El producto ya existe en el inventario'})
    category = models.CharField(
        choices=[('C', 'Cocina'), ('B', 'Bar')], default='C', max_length=1)
    buy_price = models.FloatField(default=0)
    sell_price = models.FloatField(default=0)
    is_for_sale = models.BooleanField(default=False)

    def get_ingredients(self):
        return IngredientQuantity.objects.filter(stock=self)

    def get_buy_price(self):
        return self.last_buy().per_price()

    def last_buy(self):
        return apps.get_model("transactions", "PurchaseItem").objects.filter(stock=self).latest()


    def last_price_unit(self):
        try:
            return self.last_buy().quantity.as_unit().unit()
        except apps.get_model("transactions", "PurchaseItem").DoesNotExist:
            if self.get_quantity():
                return self.get_quantity().as_unit().unit()
            else:
                return U
            
    def get_total_cost(self):
        total = self.buy_price
        for ingredient_quantity in self.get_ingredients():

            quantity = ingredient_quantity.quantity.as_unit().cast_unit(ingredient_quantity.ingredient.last_price_unit())
             
            total += ingredient_quantity.ingredient.get_total_cost() * quantity.number()

        return total

    def display_cost(self):
        if self.get_quantity():
            return str(self.get_total_cost()) + " por " + str(self.last_price_unit())
        else:
            return str(self.get_total_cost()) + " unidad"

    def get_quantity(self):
        try:
            quantity_in_stock = StockQuantity.objects.get(stock=self).quantity
            return quantity_in_stock
        except StockQuantity.DoesNotExist:
            return False

    def sell(self, quantity_sold):
        if isinstance(quantity_sold, (MeasureUnit)):
            quantity_sold = quantity_sold.as_unit()
        try:
            StockQuantity.objects.get(stock=self).sell(quantity_sold)
        except StockQuantity.DoesNotExist:
            quantity_sold = as_number(quantity_sold)
        for ingredient in IngredientQuantity.objects.filter(stock=self):
            if ingredient.quantity:
                ingredient_ammount = ingredient.quantity.as_unit()
            else:
                ingredient_ammount = ingredient.quantity

            ingredient.ingredient.sell(ingredient_ammount * quantity_sold)

    def buy(self, purchased_amount):
        if isinstance(purchased_amount, (MeasureUnit)):
            purchased_amount = purchased_amount.as_unit()
        try:
            StockQuantity.objects.get(stock=self).buy(purchased_amount)
        except StockQuantity.DoesNotExist:
            purchased_amount = as_number(purchased_amount)
        for ingredient in IngredientQuantity.objects.filter(stock=self):
            if ingredient.quantity:
                ingredient_ammount = ingredient.quantity.as_unit()
            else:
                ingredient_ammount = ingredient.quantity

            ingredient.ingredient.buy(ingredient_ammount * purchased_amount)

    class Meta:
        ordering = ['name']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.name


class MeasureUnit(models.Model):
    MEASURE_CHOICES = [
        ('kg', 'KILOGRAMO/S'),
        ('g', 'GRAMO/S'),
        ('cc', 'CENTIMETRO/S CUBICO/S'),
        ('lt', 'LITRO/S'),
        ('u', 'UNIDAD/ES')
    ]
    UNITS = {str(g): 'g', str(kg): 'kg', str(cm*cm*cm)
                 : 'cc', str(L): 'lt', str(U): 'u'}
    id = models.AutoField(primary_key=True)
    unit = models.CharField(
        max_length=2, choices=MEASURE_CHOICES, default='gr')
    quantity = models.PositiveIntegerField(default=0)

    def as_unit(self):
        units = {'g': g, 'kg': kg, 'cc': cm*cm*cm, 'lt': L, 'u': U}
        return self.quantity * units[self.unit]

    def related_units(self):
        related_units = {'g': [['kg', 'KILOGRAMO/S'],
                               ['g', 'GRAMO/S'], ], 'kg': [['kg', 'KILOGRAMO/S'],
                                                           ['g', 'GRAMO/S'], ], 'cc': [['cc', 'CENTIMETRO/S CUBICO/S'],
                                                                                       ['lt', 'LITRO/S'], ], 'lt': [['cc', 'CENTIMETRO/S CUBICO/S'],
                                                                                                                    ['lt', 'LITRO/S'], ], 'u': [['u', 'UNIDAD/ES']]}
        return related_units[self.unit]

    def substract_quantity_by_unit(self, another_unit):
        if not isinstance(another_unit, (int, Unum)):
            new_measure = self.as_unit() - another_unit.as_unit()
            self.quantity = new_measure
            self.unit = self.UNITS[str(another_unit.as_unit().unit())]
        elif isinstance(another_unit, Unum):
            new_measure = self.as_unit() - another_unit
            self.quantity = new_measure.number()
            self.unit = self.UNITS[str(new_measure.unit())]

        else:
            self.quantity = (self.quantity - another_unit)

        self.save()

    def add_quantity_by_unit(self, another_unit):
        if not isinstance(another_unit, (int, Unum)):
            new_measure = self.as_unit() + another_unit.as_unit()
            self.quantity = new_measure.number()
            self.unit = self.UNITS[str(another_unit.as_unit().unit())]
        elif isinstance(another_unit, Unum):
            new_measure = self.as_unit() + another_unit
            self.quantity = new_measure.number()
            self.unit = self.UNITS[str(new_measure.unit())]

        else:
            self.quantity = (self.quantity + another_unit)
        self.save()

    def convert_to_max_unit(self):
        if g == self.as_unit().unit():
            new_unit = self.as_unit().cast_unit(kg)
        elif cm*cm*cm == self.as_unit().unit():
            new_unit = self.as_unit().cast_unit(L)
        else:
            new_unit = self.as_unit()
        return new_unit

    def __str__(self):
        new_unit = self.convert_to_max_unit()
        return str(new_unit.number()) + " " + self.UNITS[str(new_unit.unit())]


class StockQuantity(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE, unique=True)
    quantity = models.ForeignKey(
        MeasureUnit, on_delete=models.CASCADE, null=True, blank=True)

    def sell(self, quantity_sold):
        self.quantity.substract_quantity_by_unit(quantity_sold)
        self.save()

    def buy(self, purchased_amount):
        self.quantity.add_quantity_by_unit(purchased_amount)
        self.save()

    def __str__(self):
        if (self.quantity):
            quantity = str(self.quantity)
        else:
            quantity = str(self.quantity)
        return quantity + " de " + self.stock.name


class IngredientQuantity(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Stock, on_delete=models.CASCADE, null=True, related_name="ingredient")
    quantity = models.ForeignKey(
        MeasureUnit, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        quantity = str(self.quantity.quantity) + \
            " " + self.quantity.unit

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
    number = models.IntegerField(primary_key=True, verbose_name='Numero')
    is_free = models.BooleanField(default=True)

    def __str__(self):
        return 'Mesa N°' + str(self.number)

    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'
