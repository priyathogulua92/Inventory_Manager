from django.db import models

# Create your models here.


class Sales(models.Model):
    customer_name = models.CharField(max_length=50, default='')
    date = models.DateField(default='')
    total = models.IntegerField(default=0)


class SalesItems(models.Model):
    brand = models.CharField(max_length=50, default='')
    product = models.CharField(max_length=50, default='')
    model = models.CharField(max_length=50, default='')
    price = models.IntegerField(default='')
    quantity = models.IntegerField(default='')
    amount = models.IntegerField(default=0)
    sales_id = models.ForeignKey(Sales, on_delete=models.CASCADE)


class Invoice(models.Model):
    company_name = models.CharField(max_length=150, default='')
    bill_number = models.CharField(max_length=20, default='')
    date = models.DateField(default='')
    total = models.IntegerField(default=0)


class InvoiceItems(models.Model):
    brand = models.CharField(max_length=50, default='')
    product = models.CharField(max_length=50, default='')
    model = models.CharField(max_length=50, default='')
    price = models.IntegerField(default='')
    quantity = models.IntegerField(default='')
    amount = models.IntegerField(default=0)
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)


class Inventory(models.Model):
    brand = models.CharField(max_length=50, default='')
    product = models.CharField(max_length=50, default='')
    model = models.CharField(max_length=50, default='')
    price = models.IntegerField(default='')
    quantity = models.IntegerField(default='')
