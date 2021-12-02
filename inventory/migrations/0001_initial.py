# Generated by Django 3.1.13 on 2021-12-02 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(error_messages={'unique': 'La categoria ya existe en el inventario'}, max_length=30, unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(error_messages={'unique': 'El producto ya existe en el inventario'}, max_length=30, unique=True)),
                ('quantity', models.IntegerField(default=1)),
                ('is_deleted', models.BooleanField(default=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.category')),
            ],
            options={
                'ordering': ['quantity'],
            },
        ),
    ]
