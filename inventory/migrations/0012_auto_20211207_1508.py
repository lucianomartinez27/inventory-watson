# Generated by Django 3.1.13 on 2021-12-07 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_auto_20211207_1305'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Categoria', 'verbose_name_plural': 'Categorias'},
        ),
        migrations.AlterModelOptions(
            name='ingredientquantity',
            options={'verbose_name': 'Ingrediente', 'verbose_name_plural': 'Ingredientes'},
        ),
        migrations.AlterModelOptions(
            name='stock',
            options={'ordering': ['quantity'], 'verbose_name': 'Producto', 'verbose_name_plural': 'Productos'},
        ),
        migrations.AlterModelOptions(
            name='table',
            options={'verbose_name': 'Mesa', 'verbose_name_plural': 'Mesas'},
        ),
        migrations.AlterModelOptions(
            name='waiter',
            options={'verbose_name': 'Mozo', 'verbose_name_plural': 'Mozos'},
        ),
        migrations.AlterField(
            model_name='table',
            name='number',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Numero'),
        ),
        migrations.AlterField(
            model_name='waiter',
            name='name',
            field=models.CharField(max_length=15, unique=True, verbose_name='Nombre'),
        ),
    ]