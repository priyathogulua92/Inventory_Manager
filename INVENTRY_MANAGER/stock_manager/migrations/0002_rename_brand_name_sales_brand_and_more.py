# Generated by Django 4.2.4 on 2023-08-09 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sales',
            old_name='brand_name',
            new_name='brand',
        ),
        migrations.RenameField(
            model_name='sales',
            old_name='model_Name',
            new_name='model',
        ),
    ]
