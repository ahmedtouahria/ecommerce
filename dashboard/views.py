from django.shortcuts import render
import json

from pytest import Item

from shopping.models import CategorySub, Customer, Order, OrderItem, Product, Variation
from django.db.models import Avg, Count, Min, Sum
from datetime import date, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth
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
        Order.objects.annotate(date=TruncDay("date_ordered"))
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
        "num_promotors": num_promotors
    }
    return render(request, 'dashboard/pages/dashboard.html', context)


def tables(request):
    orders = Order.objects.filter(complete=True)
    context = {"orders": orders, "titel": "orders"}

    return render(request, "dashboard/pages/tables.html", context)


def order_detail(request, pk):
    order_id = Order.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order=order_id)
    context = {"order_items": order_items,
               "order_id": order_id, "titel": "order details"}
    return render(request, 'dashboard/pages/order_detail.html', context)


def add_product(request):
    
    context = {"category": CategorySub.objects.all, "titel": "add product"}
    return render(request, 'dashboard/pages/add_product.html', context)
