# Generated by Django 3.1.13 on 2021-12-05 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20211205_2211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='waiter',
        ),
        migrations.DeleteModel(
            name='Waiter',
        ),
    ]
