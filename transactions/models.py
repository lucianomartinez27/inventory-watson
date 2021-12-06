from django.db import models
from inventory.models import Stock
from django.contrib.auth.models import User


#contains suppliers
class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12, unique=True,error_messages={'unique': u'Ya existe un proveedor con este teléfono'})
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True,error_messages={'unique': u'Ya existe un proveedor con este email'})
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name


#contains the purchase bills made
class PurchaseBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE, related_name='purchasesupplier')
    buyer = models.ForeignKey(User, on_delete = models.CASCADE, default=1)
    def __str__(self):
	    return "Venta N°: " + str(self.billno) + "realizada por " + self.buyer.username

    def get_items_list(self):
        return PurchaseItem.objects.filter(billno=self)

    def get_total_price(self):
        purchaseitems = PurchaseItem.objects.filter(billno=self)
        total = 0
        for item in purchaseitems:
            total += item.totalprice
        return total

#contains the purchase stocks made
class PurchaseItem(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE, related_name='purchasebillno')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='purchaseitem')
    buyer = models.ForeignKey(User, on_delete = models.CASCADE, default=1)
    quantity = models.IntegerField(default=1)
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)

    def __str__(self):
	    return "Venta N°: " + str(self.billno.billno) + ", Item = " + self.stock.name

class Waiter(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Table(models.Model):
    number = models.AutoField(primary_key=True)
    waiter = models.ForeignKey(Waiter,  on_delete= models.CASCADE, default=1)

    def __str__(self):
        return 'Mesa N°' + str(self.number) + " atendida por " + str(self.waiter.name)

class TableSaleBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, default=1)
    closed = models.BooleanField(default=False)
    def __str__(self):
	    return "Venta N°: " + str(self.billno) + " en mesa " + str(self.table.number)

    def get_items_list(self):
        return SaleItem.objects.filter(billno=self)
        
    def get_total_price(self):
        saleitems = self.get_items_list()
        total = 0
        for item in saleitems:
            total += item.totalprice
        return total


#contains the sale stocks made
class SaleItem(models.Model):
    billno = models.ForeignKey(TableSaleBill, on_delete = models.CASCADE, related_name='salebillno')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='saleitem')
    quantity = models.IntegerField(default=1)
    perprice = models.FloatField(default=1)
    totalprice = models.FloatField(default=1)
    def __str__(self):
	    return "Venta N°: " + str(self.billno.billno) + ", Item = " + self.stock.name

