# Generated by Django 3.1.13 on 2021-12-05 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20211203_2326'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ingredientquantity',
            unique_together={('ingredient', 'stock')},
        ),
    ]
