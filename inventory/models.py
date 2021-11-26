from django.db import models
    


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True,error_messages={'unique': u'La categoria ya existe en el inventario'})

    def __str__(self):
	    return self.name

    class Meta:
        verbose_name_plural = "categories"

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True,error_messages={'unique': u'El producto ya existe en el inventario'})
    quantity = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  null=True)

    class Meta:
        ordering = ['quantity']
  
    def __str__(self):
	    return self.name

