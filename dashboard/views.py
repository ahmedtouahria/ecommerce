from django.shortcuts import redirect, render
import json
from shopping.models import CategorySub, Customer, Order, OrderItem, Product, ProductImage, ShippingAddress, Variation
from django.db.models import Avg, Count, Min, Sum
from datetime import date, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.


def dashboard(request):
    today_mony = Product.objects.aggregate(total_price=Sum('price'))
    today_profit = Product.objects.aggregate(total_price=Sum('profit'))
    new_order = Order.objects.filter(
        date_ordered__day=date.today().day).count()
    new_clients = Customer.objects.filter(
        created_at__day=date.today().day).count()
    num_users = Customer.objects.all().count()
    num_partners = Customer.objects.filter(is_receveur=True).count()
    num_orders = Order.objects.all().count()
    num_products = Product.objects.all().count()
    num_promotors = Customer.objects.filter(is_receveur=True)
    # dashboard chart graphic
    chart_data = (
        Order.objects.annotate(date=TruncMonth("date_ordered"))
        .values("date")
        .annotate(y=Count("id"))
        .order_by("-date")
    )
    as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
    context = {
        "chart_data": as_json,
        "today_mony": today_mony,
        "today_profit": today_profit,
        "new_order": new_order,
        "new_clients": new_clients,
        "num_users": num_users,
        "num_partners": num_partners,
        "num_orders": num_orders,
        "num_products": num_products,
        "num_promotors": num_promotors,
        "titel": "Accueil"
    }
    return render(request, 'dashboard/pages/dashboard.html', context)


def tables(request):
    orders = Order.objects.filter(complete=True).order_by("-date_ordered")
    orders_no_complete = Order.objects.filter(complete=False).count()
    paginator = Paginator(orders, 12)
    page_number = request.GET.get("page", 1)
    page_products_display = paginator.get_page(page_number)
    context = {
        "orders": page_products_display,
        "titel": "orders",
        "paginator": paginator,
        "page": page_products_display,
        "page_number": int(page_number),

        "orders_no_complete": orders_no_complete}

    return render(request, "dashboard/pages/tables.html", context)


def stock(request):
    if request.method == "GET":
        query = request.GET.get("search", "")
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query))
    else:
        products = Product.objects.all().order_by("-name")
    count_products = products.count()
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page", 1)
    page_products_display = paginator.get_page(page_number)
    best_sellers = Product.objects.all().order_by("-count_sould")[:7]
    quantity_in_stock = Product.objects.aggregate(
        quantity_in_stock=Sum("quantity"))
    context = {
        "products": page_products_display,
        "titel": "stock",
        "paginator": paginator,
        "page": page_products_display,
        "page_number": int(page_number),
        "count_products": count_products,
        "best_sellers": best_sellers,
        "quantity_in_stock": quantity_in_stock,
        "categorys": CategorySub.objects.all()
    }

    return render(request, "dashboard/pages/stock.html", context)


def order_detail(request, pk):
    try:
        order_id = Order.objects.get(transaction_id=pk)
    except:
        order_id = None
    if order_id is not None:
        order_items = OrderItem.objects.filter(order=order_id)
    else:
        return redirect("tables")
    context = {"order_items": order_items,
               "order_id": order_id, "titel": "order details"}
    return render(request, 'dashboard/pages/order_detail.html', context)


def add_product(request):
    if request.method == 'POST':

        if "name" in request.POST:
            print(request.POST)
            name = request.POST.get('name', None)
            price1 = float(request.POST.get('price1', None))
            price2 = float(request.POST.get('price2', None))
            category = request.POST.get('category', None)
            quantity = int(request.POST.get('quantity', None))
            description = request.POST.get('description', None)
            images = request.FILES.getlist("images")
            image = request.FILES.get("image", None)
            print(images)
            try:
                product_duplicated = Product.objects.get(name=name)
            except Product.DoesNotExist:
                product_duplicated = None
            if product_duplicated is not None:
                pass
            else:
                try:
                    category_id = CategorySub.objects.get(name=category)
                except:
                    category_id = None
                try:
                    product = Product(name=name,
                                      category=category_id,
                                      price_achat=price1,
                                      price=price2,
                                      quantity=quantity,
                                      description=description,
                                      image=image)
                    product.save()
                    print("product_ref", product.id)
            # using session for adding product variations later
                    request.session['product_ref'] = product.id
                    for i in images:
                        p = ProductImage(product=product, image=i)
                        p.save()
                        print("success")
                except:
                    print("error")

    context = {"category": CategorySub.objects.all, "titel": "add product"}
    return render(request, 'dashboard/pages/add_product.html', context)


def edit_product(request, pk):
    if request.method == 'POST':
        if "name" in request.POST:
            name = request.POST.get('name', None)
            price1 = float(request.POST.get('price1', None))
            price2 = float(request.POST.get('price2', None))
            category = request.POST.get('category', None)
            quantity = int(request.POST.get('quantity', None))
            description = request.POST.get('description', None)
            images = request.FILES.getlist("images")
            image = request.FILES.get("image", None)
            try:
                category_id = CategorySub.objects.get(name=category)
            except:
                category_id = None
            try:
                product = Product.objects.filter(id=pk).update(name=name, category=category_id, price_achat=price1,
                                                               price=price2,
                                                               quantity=quantity,
                                                               description=description,
                                                               image=image)
                product.save()
                print("product_ref", product.id)
                # using session for adding product variations later
                request.session['product_ref_edited'] = product.id
                for i in images:
                    p = ProductImage.objects.filter(product=product).update( image=i)
                    p.save()
            except:
                print("error")

    context = {"category": CategorySub.objects.all, "titel": "add product"}
    return render(request, 'dashboard/pages/add_product.html', context)
