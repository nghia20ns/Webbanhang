# Generated by Django 4.2.7 on 2023-11-28 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_shippingaddress_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='digital',
        ),
    ]
