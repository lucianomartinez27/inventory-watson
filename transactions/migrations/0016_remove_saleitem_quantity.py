# Generated by Django 3.1.13 on 2021-12-19 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0015_auto_20211218_0225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleitem',
            name='quantity',
        ),
    ]