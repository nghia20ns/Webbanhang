# Generated by Django 4.2.7 on 2023-11-28 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_product_digital'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='is_sub',
        ),
        migrations.RemoveField(
            model_name='category',
            name='sub_category',
        ),
    ]
