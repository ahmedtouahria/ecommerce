from collections import OrderedDict
import json
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import viewsets
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ecommerce.settings import BASE_URL_YALIDIN
from shopping.models import Customer, Order, Product, Rating
from shopping.views import cookieCart
from django.http import JsonResponse
from .serializers import *

from django.contrib import messages

# Get cartItem number 
def cartitem(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItem = cookieData['cartItem']
        print("order", order)
    return cartItem

# end point to show cartItem
class cartitemApi(APIView):
    def get(self, request, format=None):
        return Response({"cartItem": cartitem(request)})


# end point to search product Ascyn

def search_products(request):
    search_data = request.GET.get('search_data', None)
    products_filtred = Product.objects.filter(name__icontains=search_data)
    data = products_filtred.values()
    return JsonResponse(list(data), safe=False)

# end point for rating product
@api_view(['POST'])
def rating_product(request):
    if request.method == 'POST':
        user_id = int(request.data['user_id'])
        product_id = int(request.data['product_id'])
        stars = int(request.data['stars'])
        content = request.data['content']
        try:
            user = Customer.objects.get(id=user_id)
            product = Product.objects.get(id=product_id)
            print(user, product)
            try:
                rate = Rating.objects.get(user=user, product=product)
                rate.stars = stars
                rate.content = content
                rate.save()
            except:
                rate = Rating.objects.create(user=user, product=product, stars=stars, content=content)

        except:
            print("except")

        return Response({"message": "Hello, world!"})


@api_view(['GET'])
def get_wilaya(request):
    headers = {"X-API-ID": settings.ID_API_YALIDIN,"X-API-TOKEN": settings.TOKEN_API_YALIDIN }
    response = requests.get(settings.BASE_URL_YALIDIN+"wilayas/", headers=headers)
    wilayas = response.json()
    result = wilayas.get('data',None)
    return Response(result)


@api_view(['GET'])
def get_cokmmuns_true(request):
    headers = {"X-API-ID": settings.ID_API_YALIDIN,"X-API-TOKEN": settings.TOKEN_API_YALIDIN }
    response = requests.get(settings.BASE_URL_YALIDIN+"communes/?has_stop_desk=true", headers=headers)
    response_delevery = requests.get(settings.BASE_URL_YALIDIN+"deliveryfees/", headers=headers)
    communs = response.json()
    deliveryfees = response_delevery.json()
    result = communs.get('data',None)
    result_2 = deliveryfees.get('data',None)

    return Response({"communs": result, "deliveryfees": result_2})
@api_view(['GET'])
def get_cokmmuns(request,pk):
    headers = {"X-API-ID": settings.ID_API_YALIDIN,"X-API-TOKEN": settings.TOKEN_API_YALIDIN }
    response = requests.get(f"{settings.BASE_URL_YALIDIN}communes/?page={pk}", headers=headers)
    communs = response.json()
    result = communs.get('data',None)

    return Response({"communs": result})

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@api_view(['POST'])
def add_product(request):
    product_ref = request.session.get("product_ref", None)
    if request.method == 'POST':
        sizes = request.data.get('sizes', None)
        colors = request.data.get('colors', None)
        if product_ref is not None:
            product = Product.objects.get(id=product_ref)
            if sizes is not None:
                for size in sizes:
                    s = Variation(product=product, category="size", item=size)
                    s.save()
            if colors is not None:
                for color in colors:
                    s = Variation(product=product,
                                  category="color", item=color)
                    s.save()
            return redirect("index")
        else:
            print("product_ref is NONE")
    return Response({"success": "true"})

# send order to yalidin express 
@api_view(['POST'])
def send_order(request):
    if request.method == 'POST':
        order_id = request.data.get("order_id", None)
        freeshipping = request.data.get("freeshipping", None)
        has_exchange = request.data.get("has_exchange", None)
        print(request.data)
        if order_id is not None:
            product_list = []
            order_obj = Order.objects.get(id=order_id)
            shipping_obj = ShippingAddress.objects.filter(order=order_obj).first()
            orders_items = OrderItem.objects.filter(order=order_id)
            for i in orders_items:
                # hundel product quantity in stock 
                product = Product.objects.get(id=i.product.id)
                product.quantity=product.quantity-i.quantity
                # add count sould in product (for statistics )
                product.count_sould=product.count_sould+i.quantity
                product.save()
                #-----PRODUCT LIST IN PARCEL--------#
                product_list.append({"produit": i.product.name, "quantité": i.quantity})
            data = OrderedDict(
                [(0,
                  OrderedDict(
                    [("order_id", str(order_obj.id)), 
                    ("firstname", shipping_obj.name),
                    ("familyname", shipping_obj.name),
                    ("contact_phone",  shipping_obj.phone),
                    ("address", shipping_obj.address),
                    ("to_commune_name", shipping_obj.city),
                    ("to_wilaya_name", shipping_obj.state),
                    ("product_list", str(product_list)),
                    ("price", int(order_obj.get_cart_total)),
                    ("freeshipping", freeshipping), ("is_stopdesk", shipping_obj.is_stopdesk), ("has_exchange", has_exchange), ("product_to_collect", str(product_list))])),])
            url = settings.BASE_URL_YALIDIN+"parcels/"
            headers = {"X-API-ID": settings.ID_API_YALIDIN,"X-API-TOKEN": settings.TOKEN_API_YALIDIN, "Content-Type": "application/json"}
            response = requests.post(url=url, headers=headers, data=json.dumps((data)))
            my_response=response.json()
            print("yalidin",my_response)
            transition_yal=my_response[str(order_id)]["tracking"]
            transaction_id=Order.objects.filter(id=order_id).update(transaction_id=transition_yal,confirmed=True,)
            print(transaction_id)
        else:
            messages.error(request,"le commande n'éxite pas")
    return Response({"success": "true"})
