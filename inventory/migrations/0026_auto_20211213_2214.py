# Generated by Django 3.1.13 on 2021-12-13 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0025_auto_20211212_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockquantity',
            name='stock',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inventory.stock'),
        ),
    ]
