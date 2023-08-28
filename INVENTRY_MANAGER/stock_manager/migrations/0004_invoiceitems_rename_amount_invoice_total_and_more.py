# Generated by Django 4.2.4 on 2023-08-23 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock_manager', '0003_remove_invoice_brand_remove_invoice_model_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(default='', max_length=50)),
                ('product', models.CharField(default='', max_length=50)),
                ('model', models.CharField(default='', max_length=50)),
                ('price', models.IntegerField(default='')),
                ('quantity', models.IntegerField(default='')),
                ('amount', models.IntegerField(default=0)),
            ],
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='amount',
            new_name='total',
        ),
        migrations.DeleteModel(
            name='Items',
        ),
        migrations.AddField(
            model_name='invoiceitems',
            name='invoice_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_manager.invoice'),
        ),
    ]