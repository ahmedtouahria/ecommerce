from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from shopping.models import *
from django.contrib import messages
from django.core.paginator import  Paginator
from django.db.models import  Count,Max
from datetime import date, timedelta
from django.utils import timezone

from shopping.utils import *

# Create your views here.
''' Nous avons deux cas ici
1/ Lorsque le client est enregistré ==>  if request.user.is_authenticated:...
2/ Lorsqu'il n'est pas inscrit ===> else:...

'''



# This function hundel all data about guest user help COOKIES and js



def index(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
        # Guest user
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItem = cookieData['cartItem']
    d=date.today()-timedelta(days=7)
    order_items = Product.objects.all().order_by("-count_sould")[:7]

    top_rated = Rating.objects.annotate(rating_count=Max("stars")).order_by("-rating_count")
    toast=ToastMessage.objects.all().last()
    affaire = Affaire.objects.all()
    context = {
        "new_arrival": Product.objects.all().reverse()[:5],
        "trending": order_items[:5],
        "top_rated": top_rated[:5],
        "toast":toast,
        "affaires":affaire,
        "category_sub": CategorySub.objects.all(),
        "category": Category.objects.all(),
        "imgs_banner": ImageBanner.objects.all()[:3],
        "products": Product.objects.all()[:12],
        "items": items,
        "order": order,
        "cartItem": cartItem,
        "titel": "Accueil",

    }
    return render(request, 'pages/home.html', context)
# products views

# la page des produits


def products(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
        print(items)
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItem = cookieData['cartItem']
    products = Product.objects.filter(quantity__gt=0)
    paginator = Paginator(products,8)
    page_number=request.GET.get("page",1)
    page_products_display=paginator.get_page(page_number)
    context = {
        "products": page_products_display,
        "categorys": Category.objects.all(),
        "order": order,
        "cartItem": cartItem,
        "paginator":paginator,
        "page":page_products_display,
        "page_number":int(page_number),
         "titel": "produits",


    }
    return render(request, 'pages/products.html', context)

# la page d'un seule produit


def product(request, pk):
    # print("customer_ref",request.session['ref_customer'])

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
        print(items)
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItem = cookieData['cartItem']
    try:
        product_id = Product.objects.get(slug=pk)
    except Product.DoesNotExist:
        product_id = None
        return redirect('products')
    context = {
        "products": Product.objects.filter(category=product_id.category),
        "ratings": Rating.objects.filter(product=product_id),
        "stars": product_id.avg_rating,
        "product": product_id,
        "order": order,
        "cartItem": cartItem,
        "product_imgs":ProductImage.objects.filter(product=product_id),
        "titel": str(product_id.name).replace(" ", "-").lower(),

    }
    return render(request, 'pages/single-product.html', context)
# register Customer views


def productWithCode(request, pk, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    print("ip", get_client_ip(request))
    request.session['client_ip'] = []
   # client_ip=get_client_ip(request)
    try:
        customer = Customer.objects.get(code=code)
        request.session['ref_customer'] = customer.id

        # request.session['client_ip'] = get_client_ip(request)
        # print("customer_ref", request.session['ref_customer'])
    except:
        request.session['ref_customer'] = None
        print("customer_ref", request.session['ref_customer'])

    print("code : ", code)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
        print(items)
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItem = cookieData['cartItem']
    try:
        product_id = Product.objects.get(slug=pk)
    except Product.DoesNotExist:
        product_id = None
        return redirect('products')
    context = {
        "products": Product.objects.filter(category=product_id.category),
        "ratings": Rating.objects.filter(product=product_id),
        "stars": product_id.avg_rating,
        "product": product_id,
        "order": order,
        "cartItem": cartItem,
        "product_imgs":ProductImage.objects.filter(product=product_id),
        "titel": str(product_id.name).replace(" ", "-").lower(),
    }
    return render(request, 'pages/single-product.html', context)


''' AUTHENTICATION LOGIC
LogIn / SignUp / Logout
'''
# la page d'inscription


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        name = request.POST['username']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
       # print(name,phone,password1,password2)
        if len(name) > 5 and len(phone) == 10 and len(password1) >= 8 and password1 == password2:
            list_users = Customer.objects.filter(name=name)
            if list_users.count() < 1:
                user = Customer.objects.create(
                    name=name, phone=phone, password=password1)
                login(request, user)
                messages.success(request, "register user successfully")
                return redirect('index')
        messages.error(
            request, "Unsuccessful registration. Invalid information.")

    return render(request, 'dashboard/pages/sign-up.html')
# login Customer views

# la page d'authentication (Login)


def login_customer(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        if len(phone) == 10 and len(password) > 8:
            user = authenticate(phone=phone, password=password)

            if user is not None:
                login(request, user)
                if user.admin:
                    return redirect('/admin/')
                messages.info(
                    request, f"You are now logged in as {user.name}.")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'dashboard/pages/login.html')


@login_required(login_url='login')
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")


'''
-------------------
Profits page Logic
-------------------
'''


@login_required(login_url='login')
def profile(request):
    user = request.user
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
        # print(items)
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItem = cookieData['cartItem']
    try:
        money = Conversion.objects.get(receveur=user)
    except Conversion.DoesNotExist:
        money = 0
    context={
        "money": money,
        "titel": "profile",
        "items": items,
        "order": order,
        "cartItem": cartItem,
         
         }
    return render(request, "pages/myprofile.html",context )


@login_required(login_url='login')
def profile_orders(request):
    user = request.user
    orders = Order.objects.filter(
        customer=user, complete=True).order_by('-date_ordered')
    paginator = Paginator(orders,8)
    page_number=request.GET.get("page",1)
    page_products_display=paginator.get_page(page_number)


    context = {
        "orders": page_products_display,
        "titel": "Mes commandes",
        "page":page_products_display,
        "page_number":int(page_number),

        "paginator":paginator,

    }
    return render(request, 'pages/profile_orders.html', context)


def myorders(request, pk):
    user = request.user
    order = Order.objects.filter(transaction_id=pk).first()
    headers = {"X-API-ID": settings.ID_API_YALIDIN,"X-API-TOKEN": settings.TOKEN_API_YALIDIN }
    response = requests.get(f"{settings.BASE_URL_YALIDIN}parcels/{order.transaction_id}", headers=headers)
    parcel = response.json()
    print(parcel)
    total_data=parcel.get("total_data",None)
    if total_data > 0:
        transaction_id = parcel.get('data',None)
        last_status= transaction_id[0]
        try:
            if order.customer != user:
                return redirect("profile_orders")
        except:
            return redirect("profile_orders")
        order_items = OrderItem.objects.filter(order=order)
    else:
        order_items = OrderItem.objects.filter(order=order)
        last_status=""
        messages.info(request,"Cette demande est en attente!")
    context = {
        "order": order,
        "order_items": order_items,
        "titel": "Mes commandes",
        "last_status":last_status
    }
    return render(request, 'pages/profile_myorder.html', context)


# card product views
# la page de gestionaire de panier d'un client

def card(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
        # print(items)
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItem = cookieData['cartItem']
        print("order", order)
    context = {
        "items": items,
        "order": order,
        "cartItem": cartItem,
        "titel": "panier"

    }
    return render(request, 'pages/card.html', context)
# checkout order views

# la page de Processus de vente


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
        # print(items)
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItem = cookieData['cartItem']

    context = {
        "items": items,
        "order": order,
        "cartItem": cartItem,
        "titel": "vérifier"
    }
    return render(request, 'pages/checkout.html', context)

# endpoint to update cart_item number for user authenticated


def updateItem(request):
    # get user
    customer = request.user
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    # load json request from user
    data = json.loads(request.body)
    if "productColor" in data or "productSize" in data:
        productColor = data.get("productColor",None)
        productSize = data.get("productSize",None)
        productId = data['productId']
        action = data['action']
        product = Product.objects.filter(id=productId).first()
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(
            order=order, product=product, color=productColor, size=productSize)
        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()
    else:
        # get required data from json  "productId" & "action user (add,remove)"
        productId = data['productId']
        action = data['action']
        print('Action:', action)
        print('Product:', productId)
        product = Product.objects.filter(id=productId).first()
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(
            order=order, product=product)
        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    data = json.loads(request.body)
    print(data)
    stop_disk=data.get("stop_desk",False)
    # get order if user is authenticated
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    # get order if user is not authenticated
    else:
        customer, order = guestOrder(request, data)
    # get ref_customer (user shared product)

    try:
        user_id = request.session['ref_customer']
        user_recommended = Customer.objects.get(id=user_id)
    except:
        user_recommended = None
    if user_recommended is not None and request.user != user_recommended and order is not None:
        order.recommended_by = user_recommended
        order.save()
        user_recommended.point += 1
        user_recommended.number_of_referalls += 1
        user_recommended.is_receveur = True
        user_recommended.save()
    if customer is not None:
        total = float(data['form']['total'])
        print("total", total, "order.get_cart_total ", order.get_cart_total)
        if total > 0:
            order.complete = True
            order.save()
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                name=data['form']['name'],
                phone=data['form']['phone'],
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                is_stopdesk=stop_disk
            )

    else:
        redirect("login")
    return JsonResponse('Payment submitted..', safe=False)
