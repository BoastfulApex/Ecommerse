# Generated by Django 3.2.4 on 2021-08-21 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_rename_name_customer_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='password',
        ),
    ]
