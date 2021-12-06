# Generated by Django 3.1.13 on 2021-12-03 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(error_messages={'unique': 'El ingrediente ya existe en el inventario'}, max_length=30, unique=True)),
                ('ammount', models.IntegerField(default=1)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.stock')),
            ],
        ),
    ]