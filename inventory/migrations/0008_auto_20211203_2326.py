# Generated by Django 3.1.13 on 2021-12-03 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_ingredientquantity_ingredient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='price',
            new_name='buy_price',
        ),
        migrations.AddField(
            model_name='stock',
            name='sell_price',
            field=models.FloatField(default=0),
        ),
    ]
