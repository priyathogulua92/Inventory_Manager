# Generated by Django 4.2.4 on 2023-08-24 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock_manager', '0004_invoiceitems_rename_amount_invoice_total_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sales',
            old_name='amount',
            new_name='total',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='model',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='price',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='product',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='inventory',
            name='brand',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='model',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='product',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='sales',
            name='customer_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='sales',
            name='date',
            field=models.DateField(default=''),
        ),
        migrations.CreateModel(
            name='SalesItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(default='', max_length=50)),
                ('product', models.CharField(default='', max_length=50)),
                ('model', models.CharField(default='', max_length=50)),
                ('price', models.IntegerField(default='')),
                ('quantity', models.IntegerField(default='')),
                ('amount', models.IntegerField(default=0)),
                ('sales_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_manager.sales')),
            ],
        ),
    ]