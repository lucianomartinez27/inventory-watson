# Generated by Django 3.1.13 on 2021-12-03 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20211203_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientquantity',
            name='ingredient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='inventory.stock'),
        ),
    ]