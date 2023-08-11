from django.shortcuts import render
from django.http import HttpResponse
from .models import Sales
from .models import Inventory
from .models import Invoice
from django.core import exceptions


def sales(request):
    if request.GET:
        qcustomer_name = '.*'
        qdate = '.*'
        qbrand = '.*'
        qmodel = '.*'
        qproduct = '.*'
        customer_name = str(request.GET['cust_name']).upper()
        date = request.GET['date']
        brand = str(request.GET['brand']).upper()
        product = str(request.GET['product']).upper()
        model = str(request.GET['model']).upper()
        if customer_name:
            qcustomer_name = customer_name
        elif date:
            qdate = date
        elif brand:
            qbrand = brand
        elif model:
            qmodel = model
        elif product:
            qproduct = product

        sales_list = Sales.objects.filter(customer_name__iregex=rf'{qcustomer_name}', date__iregex=rf'{qdate}',
                                          brand__iregex=rf'{qbrand}', model__iregex=rf'{qmodel}', product__iregex=rf'{qproduct}')
        return render(request, 'sales.html', {'sales_list': sales_list})

    elif request.method == "POST" and request.POST:
        if (request.POST['Cust_name'] == "" or request.POST["Date"] == "" or request.POST["Brand"] == "" or request.POST["Product"] == "" or request.POST["Model"] == "" or request.POST["Price"] == "" or request.POST["Quantity"] == ""):
            return render(request, 'sales.html', {'error': "All inputs are mandatory"})

        sales1 = Sales()
        sales1.customer_name = (request.POST["cust_name"]).upper()
        sales1.date = (request.POST["date"])
        sales1.brand = (request.POST["brand"]).upper()
        sales1.product = (request.POST["product"]).upper()
        sales1.model = (request.POST["model"]).upper()
        sales1.price = int(request.POST["price"])
        sales1.quantity = int(request.POST["quantity"])
        sales1.amount = int(sales1.price*sales1.quantity)
        try:
            inventryObj = Inventory.objects.get(
                brand=sales1.brand, product=sales1.product, model=sales1.model)
            if inventryObj.quantity < sales1.quantity:
                return render(request, 'sales.html', {'error': "Only {} stock available for item {} {} {} ".format(inventryObj.quantity, sales1.brand, sales1.product, sales1.model)})
            inventryObj.quantity -= sales1.quantity
            inventryObj.save()
            sales1.save()

        except Inventory.DoesNotExist:
            return render(request, 'sales.html', {'error': "{} {} {} stock not available".format(sales1.brand, sales1.product, sales1.model)})
        except Inventory.MultipleObjectsReturned:
            return render(request, 'sales.html', {'error': "{} {} {} Multiple entry of same product is there".format(sales1.brand, sales1.product, sales1.model)})

    sales_list = Sales.objects.all().order_by('-date')[:10]
    return render(request, 'sales.html', {'sales_list': sales_list})


def invoice(request):
    if request.GET:
        qcompany_name = '.*'
        qbill_number = '.*'
        qdate = '.*'
        qbrand = '.*'
        qmodel = '.*'
        qproduct = '.*'
        company_name = str(request.GET['company_name']).upper()
        bill_number = str(request.GET['bill_number']).upper()
        date = (request.GET['date'])
        brand = str(request.GET['brand']).upper()
        product = str(request.GET['product']).upper()
        model = str(request.GET['model']).upper()

        if company_name:
            qcompany_name = company_name
        elif bill_number:
            qbill_number = bill_number
        elif date:
            qdate = date
        elif brand:
            qbrand = brand
        elif model:
            qmodel = model
        elif product:
            qproduct = product

        invoice_list = Invoice.objects.filter(company_name__iregex=rf'{qcompany_name}', bill_number__iregex=rf'{qbill_number}', date__iregex=rf'{qdate}',
                                              brand__iregex=rf'{qbrand}', model__iregex=rf'{qmodel}', product__iregex=rf'{qproduct}')
        return render(request, 'invoice.html', {'invoice_list': invoice_list})

    elif request.method == 'POST' and request.POST:
        if (request.POST["company_name"] == "" or request.POST["bill_number"] == "" or request.POST["date"] == "" or request.POST["brand"] == "" or request.POST["product"] == "" or request.POST["model"] == "" or request.POST["price"] == "" or request.POST["quantity"] == ""):
            return render(request, 'invoice.html', {'error': "All inputs are mandatory"})

        invoice1 = Invoice()
        invoice1.company_name = str(request.POST['company_name']).upper()
        invoice1.bill_number = str(request.POST['bill_number']).upper()
        invoice1.date = request.POST['date']
        invoice1.brand = str(request.POST['brand']).upper()
        invoice1.product = str(request.POST['product']).upper()
        invoice1.model = str(request.POST['model']).upper()
        invoice1.price = int(request.POST['price'])
        invoice1.quantity = int(request.POST['quantity'])
        invoice1.amount = int(invoice1.price*invoice1.quantity)
        try:
            inventoryObj = Inventory.objects.get(
                brand=invoice1.brand, product=invoice1.product, model=invoice1.model)
            inventoryObj.quantity += invoice1.quantity
            inventoryObj.price = invoice1.price
            inventoryObj.save()
            invoice1.save()
        except Inventory.DoesNotExist:
            inventoryObj = Inventory()
            inventoryObj.brand = invoice1.brand
            inventoryObj.product = invoice1.product
            inventoryObj.model = invoice1.model
            inventoryObj.price = invoice1.price
            inventoryObj.quantity = invoice1.quantity
            inventoryObj.save()
            invoice1.save()
        except Inventory.MultipleObjectsReturned:
            return render(request, 'invoice.html', {'error': "{} {} {} Multiple entry of same product is there".format(invoice1.brand, invoice1.product, invoice1.model)})
    invoice_list = Invoice.objects.all().order_by('-date')[:10]
    return render(request, 'invoice.html', {'invoice_list': invoice_list})


def inventory(request):
    if request.GET:
        qbrand = '.*'
        qmodel = '.*'
        qproduct = '.*'
        brand = str(request.GET['brand']).upper()
        product = str(request.GET['product']).upper()
        model = str(request.GET['model']).upper()
        if brand:
            qbrand = brand
        elif model:
            qmodel = model
        elif product:
            qproduct = product
        inventory_list = Inventory.objects.filter(
            brand__iregex=rf'{qbrand}', model__iregex=rf'{qmodel}', product__iregex=rf'{qproduct}')
        return render(request, 'inventory.html', {'inventory_list': inventory_list})
    inventory_list = Inventory.objects.all().order_by('brand')[:10]
    return render(request, 'inventory.html', {'inventory_list': inventory_list})
