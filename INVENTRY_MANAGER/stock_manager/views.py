from django.shortcuts import render
from django.http import HttpResponse
from .models import Sales
from .models import SalesItems
from .models import Inventory
from .models import Invoice
from .models import InvoiceItems
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

        sales_list = SalesItems.objects.filter(sales_id__customer_name__iregex=rf'{qcustomer_name}', sales_id__date__iregex=rf'{qdate}',
                                               brand__iregex=rf'{qbrand}', model__iregex=rf'{qmodel}', product__iregex=rf'{qproduct}')
        return render(request, 'sales.html', {'sales_list': sales_list})

    elif request.method == "POST" and request.POST:
        if (request.POST['cust_name'] == "" or request.POST["date"] == "" or request.POST["brand"] == "" or request.POST["product"] == "" or request.POST["model"] == "" or request.POST["price"] == "" or request.POST["quantity"] == ""):
            return render(request, 'sales.html', {'error': "All inputs are mandatory"})

        brand_list = []
        product_list = []
        model_list = []
        price_list = []
        quantity_list = []

        brand_list = request.POST.getlist("brand")
        product_list = request.POST.getlist("product")
        model_list = request.POST.getlist("model")
        price_list = request.POST.getlist("price")
        quantity_list = request.POST.getlist("quantity")
        total_amount = 0

        for i in range(0, len(model_list)):
            brand = str(brand_list[i]).upper()
            product = str(product_list[i]).upper()
            model = str(model_list[i]).upper()
            quantity = int(quantity_list[i])
            try:
                inventryObj = Inventory.objects.get(
                    brand=brand, product=product, model=model)
                if inventryObj.quantity < quantity:
                    return render(request, 'sales.html', {'error': "Only {} stock available for item {} {} {} ".format(inventryObj.quantity, brand, product, model)})
            except Inventory.DoesNotExist:
                return render(request, 'sales.html', {'error': "{} {} {} stock not available".format(brand, product, model)})
            except Inventory.MultipleObjectsReturned:
                return render(request, 'sales.html', {'error': "{} {} {} Multiple entry of same product is there".format(brand, product, model)})

        sales1 = Sales()
        sales1.customer_name = (request.POST["cust_name"]).upper()
        sales1.date = (request.POST["date"])
        sales1.save()

        for i in range(0, len(brand_list)):
            items1 = SalesItems()
            items1.brand = str(brand_list[i]).upper()
            items1.product = str(product_list[i]).upper()
            items1.model = str(model_list[i]).upper()
            items1.price = int(price_list[i])
            items1.quantity = int(quantity_list[i])
            items1.amount = items1.price*items1.quantity
            items1.sales_id = sales1
            total_amount += items1.price*items1.quantity
            items1.save()
            try:
                inventryObj = Inventory.objects.get(
                    brand=items1.brand, product=items1.product, model=items1.model)
                if inventryObj.quantity < items1.quantity:
                    return render(request, 'sales.html', {'error': "Only {} stock available for item {} {} {} ".format(inventryObj.quantity, items1.brand, items1.product, items1.model)})
                inventryObj.quantity -= items1.quantity
                inventryObj.save()

            except Inventory.DoesNotExist:
                return render(request, 'sales.html', {'error': "{} {} {} stock not available".format(items1.brand, items1.product, items1.model)})
            except Inventory.MultipleObjectsReturned:
                return render(request, 'sales.html', {'error': "{} {} {} Multiple entry of same product is there".format(items1.brand, items1.product, items1.model)})
        sales1.total = total_amount
        sales1.save()
    sales_list = SalesItems.objects.all().order_by('-sales_id__date')[:10]
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

        invoice_list = InvoiceItems.objects.filter(invoice_id__company_name__iregex=rf'{qcompany_name}', invoice_id__bill_number__iregex=rf'{qbill_number}', invoice_id__date__iregex=rf'{qdate}',
                                                   brand__iregex=rf'{qbrand}', model__iregex=rf'{qmodel}', product__iregex=rf'{qproduct}')
        return render(request, 'invoice.html', {'invoice_list': invoice_list})

    elif request.method == 'POST' and request.POST:
        if (request.POST["company_name"] == "" or request.POST["bill_number"] == "" or request.POST["date"] == "" or request.POST["brand"] == "" or request.POST["product"] == "" or request.POST["model"] == "" or request.POST["price"] == "" or request.POST["quantity"] == ""):
            return render(request, 'invoice.html', {'error': "All inputs are mandatory"})

        invoice1 = Invoice()
        invoice1.company_name = str(request.POST['company_name']).upper()
        invoice1.bill_number = str(request.POST['bill_number']).upper()
        invoice1.date = request.POST['date']

        brand_list = []
        product_list = []
        model_list = []
        price_list = []
        quantity_list = []

        brand_list = request.POST.getlist("brand")
        product_list = request.POST.getlist("product")
        model_list = request.POST.getlist("model")
        price_list = request.POST.getlist("price")
        quantity_list = request.POST.getlist("quantity")
        total_amount = 0
        invoice1.save()

        for i in range(0, len(brand_list)):
            items1 = InvoiceItems()
            items1.brand = str(brand_list[i]).upper()
            items1.product = str(product_list[i]).upper()
            items1.model = str(model_list[i]).upper()
            items1.price = int(price_list[i])
            items1.quantity = int(quantity_list[i])
            items1.amount = items1.price*items1.quantity
            items1.invoice_id = invoice1
            total_amount += items1.price*items1.quantity
            items1.save()
            try:
                inventoryObj = Inventory.objects.get(
                    brand=items1.brand, product=items1.product, model=items1.model)
                inventoryObj.quantity += items1.quantity
                inventoryObj.price = items1.price
                inventoryObj.save()
            except Inventory.DoesNotExist:
                inventoryObj = Inventory()
                inventoryObj.brand = items1.brand
                inventoryObj.product = items1.product
                inventoryObj.model = items1.model
                inventoryObj.price = items1.price
                inventoryObj.quantity = items1.quantity
                inventoryObj.save()
            except Inventory.MultipleObjectsReturned:
                return render(request, 'invoice.html', {'error': "{} {} {} Multiple entry of same product is there".format(items1.brand, items1.product, items1.model)})
        invoice1.total = total_amount
        invoice1.save()
    invoice_list = InvoiceItems.objects.all().order_by(
        '-invoice_id__date')[:10]
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
