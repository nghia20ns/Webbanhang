# Generated by Django 4.2.7 on 2023-11-27 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_product_detail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='city',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='state',
        ),
    ]
