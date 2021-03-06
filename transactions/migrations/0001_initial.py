# Generated by Django 3.1.13 on 2021-12-21 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseBill',
            fields=[
                ('billno', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('buyer', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Factura de compra',
                'verbose_name_plural': 'Facturas de compra',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('phone', models.CharField(error_messages={'unique': 'Ya existe un proveedor con este teléfono'}, max_length=12, unique=True)),
                ('address', models.CharField(max_length=200)),
                ('email', models.EmailField(error_messages={'unique': 'Ya existe un proveedor con este email'}, max_length=254, unique=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
            },
        ),
        migrations.CreateModel(
            name='TableSaleBill',
            fields=[
                ('billno', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('closed', models.BooleanField(default=False)),
                ('table', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inventory.table')),
                ('waiter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inventory.waiter')),
            ],
            options={
                'verbose_name': 'Venta en mesa',
                'verbose_name_plural': 'Ventas en mesa',
            },
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perprice', models.FloatField(default=1)),
                ('totalprice', models.FloatField(default=1)),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salebillno', to='transactions.tablesalebill')),
                ('quantity_of', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.measureunit')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saleitem', to='inventory.stock')),
            ],
            options={
                'verbose_name': 'Item de venta',
                'verbose_name_plural': 'Items de venta',
            },
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perprice', models.IntegerField(default=1)),
                ('totalprice', models.IntegerField(default=1)),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchasebillno', to='transactions.purchasebill')),
                ('buyer', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('quantity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.measureunit')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchaseitem', to='inventory.stock')),
            ],
            options={
                'verbose_name': 'Item de compra',
                'verbose_name_plural': 'Items de compra',
                'get_latest_by': 'billno__time',
            },
        ),
        migrations.AddField(
            model_name='purchasebill',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchasesupplier', to='transactions.supplier'),
        ),
    ]
