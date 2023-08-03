from django.shortcuts import render
from django.http import HttpResponse
from .models import Sales
from .models import Inventory
from .models import Invoice
from django.core import exceptions


def sales(request):
    if request.method == "POST":
        sales1 = Sales()
        sales1.customer_name = (request.POST["Cust_name"]).upper()
        sales1.date = (request.POST["Date"])
        sales1.brand_name = (request.POST["Brand_name"]).upper()
        sales1.product = (request.POST["Product"]).upper()
        sales1.model_Name = (request.POST["Model_name"]).upper()
        sales1.price = int(request.POST["Price"])
        sales1.quantity = int(request.POST["Quantity"])
        sales1.amount = int(sales1.price*sales1.quantity)
        try:
            inventryObj = Inventory.objects.get(
                brand=sales1.brand_name, product=sales1.product, model=sales1.model_Name)
            print("Before: ", inventryObj.quantity)
            if inventryObj.quantity < sales1.quantity:
                return render(request, 'sales.html', {'error': "Only {} stock available for item {} {} {} ".format(inventryObj.quantity, sales1.brand_name, sales1.product, sales1.model_Name)})
            inventryObj.quantity -= sales1.quantity
            print("After: ", inventryObj.quantity)
            inventryObj.save()
            sales1.save()

        except Inventory.DoesNotExist:
            return render(request, 'sales.html', {'error': "{} {} {} stock not available".format(sales1.brand_name, sales1.product, sales1.model_Name)})
        except Inventory.MultipleObjectsReturned:
            return render(request, 'sales.html', {'error': "{} {} {} Multiple entry of same product is there".format(sales1.brand_name, sales1.product, sales1.model_Name)})

    sales_list = Sales.objects.all().order_by('-date')[:10]
    return render(request, 'sales.html', {'sales_list': sales_list})


def invoice(request):
    if request.method == 'POST':
        print("Inside POST + ", request)
        invoice1 = Invoice()
        invoice1.company_name = str(request.POST['COMPANY_NAME']).upper()
        invoice1.bill_number = int(request.POST['BILL_NUMBER'])
        invoice1.date = request.POST['DATE']
        invoice1.brand = str(request.POST['BRAND']).upper()
        invoice1.product = str(request.POST['PRODUCT']).upper()
        invoice1.model = str(request.POST['MODEL']).upper()
        invoice1.price = int(request.POST['PRICE'])
        invoice1.quantity = int(request.POST['QUANTITY'])
        invoice1.amount = int(invoice1.price*invoice1.quantity)
        try:
            dbInventoryQs = Inventory.objects.get(
                brand=invoice1.brand, product=invoice1.product, model=invoice1.model)
            print("Before quantity: ", dbInventoryQs.quantity)
            dbInventoryQs.quantity += invoice1.quantity
            print("After quantity: ", dbInventoryQs.quantity)
            dbInventoryQs.save()
            invoice1.save()
        except Inventory.DoesNotExist:
            inventoryObj = Inventory()
            inventoryObj.brand = invoice1.brand
            inventoryObj.product = invoice1.product
            inventoryObj.model = invoice1.model
            inventoryObj.price = invoice1.price
            inventoryObj.quantity = invoice1.quantity
            print("Creating new entry")
            inventoryObj.save()
            invoice1.save()
        except Inventory.MultipleObjectsReturned:
            return render(request, 'invoice.html', {'error': "{} {} {} Multiple entry of same product is there".format(invoice1.brand, invoice1.product, invoice1.model)})

    invoice_list = Invoice.objects.all().order_by('-date')[:10]
    return render(request, 'invoice.html', {'invoice_list': invoice_list})


def inventory(request):
    print("First GET ", request.GET)
    if request.GET:
        brand = str(request.GET['BRAND']).upper()
        product = str(request.GET['PRODUCT']).upper()
        model = str(request.GET['MODEL']).upper()
        if len(brand) == 0 and len(product) == 0 and len(model) == 0:
            dbInventoryQs = Inventory.objects.all().order_by("brand")[:10]

        elif len(brand) > 0 and len(product) > 0 and len(model) > 0:
            dbInventoryQs = Inventory.objects.filter(
                brand=brand, product=product, model=model)

        elif len(brand) > 0 and len(product) > 0:
            dbInventoryQs = Inventory.objects.filter(
                brand=brand, product=product)

        elif len(brand) > 0 and len(model) > 0:
            dbInventoryQs = Inventory.objects.filter(brand=brand, model=model)

        elif len(product) > 0 and len(model) > 0:
            dbInventoryQs = Inventory.objects.filter(
                product=product, model=model)

        elif len(brand) > 0:
            dbInventoryQs = Inventory.objects.filter(brand=brand)

        elif len(product) > 0:
            dbInventoryQs = Inventory.objects.filter(product=product)

        elif len(model) > 0:
            dbInventoryQs = Inventory.objects.filter(model=model)

    else:
        dbInventoryQs = Inventory.objects.all().order_by('brand')[:10]
    return render(request, 'inventory.html', {'inventoryData': dbInventoryQs})
