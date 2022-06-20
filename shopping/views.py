from typing import List
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from shopping.models import *
from django.contrib import messages
from django.core.paginator import  Paginator
# Create your views here.
''' Nous avons deux cas ici
1/ Lorsque le client est enregistré ==>  if request.user.is_authenticated:...
2/ Lorsqu'il n'est pas inscrit ===> else:...

'''


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# This function hundel all data about guest user help COOKIES and js


def cookieCart(request):

    # Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('cart', cart)
    items = []
    order = {"get_cart_total": 0, "get_cart_items": 0}
    cartItem = order['get_cart_items']
    for i in cart:
        try:
            cartItem += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price*cart[i]['quantity'])
            order['get_cart_total'] += total
            try:
                item = {
                    'id': product.id,
                    'product': {'id': product.id, 'name': product.name, 'price': product.price,
                                'image': product.image}, 'quantity': cart[i]['quantity'], 'color': cart[i]["color"], 'size': cart[i]["size"],
                    'get_total': total,
                }
            except:
                item = {
                    'id': product.id,
                    'product': {'id': product.id, 'name': product.name, 'price': product.price,
                                'image': product.image}, 'quantity': cart[i]['quantity'],
                    'get_total': total,
                }
            items.append(item)

        except Product.DoesNotExist:
            print("Product.DoesNotExist")
    return {'cartItem': cartItem, 'order': order, 'items': items}


def guestOrder(request, data):
    name = data['form']['name']
    phone = data['form']['phone']
    cookieData = cookieCart(request)
    items = cookieData['items']
    print("items", items)
    customer, created = Customer.objects.get_or_create(phone=phone, )
    customer.name = name
    customer.save()
    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        print("item", item)
        product = Product.objects.filter(id=item['id']).first()
        try:
            OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity'],
                color=item['color'],
                size=item['size']
            )
        except :
            OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity'],
            )
    try:
        return customer, order
    except:
        return None, None


def index(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
        print(cartItem)
        # Guest user
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItem = cookieData['cartItem']
    context = {
        "new_arrival": Product.objects.all()[:5],
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
    products = Product.objects.all()
    paginator = Paginator(products,6)
    page_number=request.GET.get("page",1)
    page_products_display=paginator.get_page(page_number)
    print("page number ",page_number)
    context = {
        "products": page_products_display,
        "categorys": Category.objects.all(),
        "order": order,
        "cartItem": cartItem,
        "paginator":paginator,
        "page_number":page_number,
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
        product_id = Product.objects.get(id=pk)
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
    context = {
        "product": Product.objects.get(id=pk),
        "order": order,
        "cartItem": cartItem,
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

    return render(request, 'pages/register.html')
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
    return render(request, 'pages/login.html')


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
    try:
        money = Conversion.objects.get(receveur=user)
    except Conversion.DoesNotExist:
        money = 0
    return render(request, "pages/myprofile.html", {"money": money, "titel": "profile"})


@login_required(login_url='login')
def profile_orders(request):
    user = request.user
    orders = Order.objects.filter(
        customer=user, complete=True).order_by('-date_ordered')

    context = {
        "orders": orders,
        "titel": "Mes commandes"


    }
    return render(request, 'pages/profile_orders.html', context)


def myorders(request, pk):
    order = Order.objects.filter(id=pk).first()
    order_items = OrderItem.objects.filter(order=order)
    context = {
        "order": order,
        "order_items": order_items,
        "titel": "Mes commandes"

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
    if "productColor" in data:
        productColor = data['productColor']
        productSize = data['productSize']
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
    # print("process_o_c",request.session['ref_customer'])
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
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        redirect("login")
    return JsonResponse('Payment submitted..', safe=False)
