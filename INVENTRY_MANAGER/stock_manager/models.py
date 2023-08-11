from django.db import models

# Create your models here.


class Sales(models.Model):
    customer_name = models.CharField(max_length=50)
    date = models.DateField()
    brand = models.CharField(max_length=20)
    product = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class Invoice(models.Model):
    company_name = models.CharField(max_length=150, default='')
    bill_number = models.CharField(max_length=20, default='')
    date = models.DateField(default='')
    brand = models.CharField(max_length=50, default='')
    product = models.CharField(max_length=50, default='')
    model = models.CharField(max_length=50, default='')
    price = models.IntegerField(default='')
    quantity = models.IntegerField(default='')
    amount = models.IntegerField(default=0)


class Inventory(models.Model):
    brand = models.CharField(max_length=20, default='')
    product = models.CharField(max_length=20, default='')
    model = models.CharField(max_length=20, default='')
    price = models.IntegerField(default='')
    quantity = models.IntegerField(default='')
