# Generated by Django 3.1.13 on 2021-12-07 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_table_waiter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='number',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]