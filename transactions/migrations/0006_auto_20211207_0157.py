# Generated by Django 3.1.13 on 2021-12-07 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_table_is_free'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablesalebill',
            name='name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='transactions.waiter'),
        ),
    ]
