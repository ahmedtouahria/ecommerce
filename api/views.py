from collections import OrderedDict
import json
from django.shortcuts import redirect
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from shopping.models import Customer, Order, Product, Rating
from shopping.views import cookieCart
from .serializers import *
from constance import config
from django.contrib import messages
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa


# Get cartItem number 
def cartitem(request):
    if request.user.is_authenticated:
        customer = request.user
        order_changed = request.session.get("order_changed_id", None)
        if order_changed is not None:
            order = Order.objects.get(customer=customer,transaction_id=order_changed)
            order.confirmed=False
            order.save()
        else:
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItem = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItem = cookieData['cartItem']
    return cartItem

# end point to show cartItem
class cartitemApi(APIView):
    def get(self, request, format=None):
        return Response({"cartItem": cartitem(request)})


# end point to search product Ascyn



# end point for rating product
@api_view(['POST'])
def rating_product(request):
    if request.method == 'POST':
        user_id = request.data.get("user_id",None)
        product_id = request.data.get("product_id",None)
        stars = request.data.get("stars",4)
        content = request.data.get("content")
        try:
            user = Customer.objects.get(id=user_id)
            product = Product.objects.get(id=product_id)
            print(user, product)
            rate,create = Rating.objects.get_or_create(user=user, product=product)
            rate.stars = stars
            rate.content = content
            rate.save()
        except:
            print("Exception for rating system ")

        return Response({"message": "Hello, world!"})


@api_view(['GET'])
def get_wilaya(request):
    headers = {"X-API-ID": config.ID_API_YALIDIN,"X-API-TOKEN": config.TOKEN_API_YALIDIN }
    response = requests.get(config.BASE_URL_YALIDIN+"wilayas/", headers=headers)
    wilayas = response.json()
    result = wilayas.get('data',None)
    return Response(result)


@api_view(['GET'])
def get_cokmmuns_true(request):
    headers = {"X-API-ID": config.ID_API_YALIDIN,"X-API-TOKEN": config.TOKEN_API_YALIDIN }
    response = requests.get(config.BASE_URL_YALIDIN+"communes/?has_stop_desk=true", headers=headers)
    response_delevery = requests.get(config.BASE_URL_YALIDIN+"deliveryfees/", headers=headers)
    communs = response.json()
    deliveryfees = response_delevery.json()
    result = communs.get('data',None)
    result_2 = deliveryfees.get('data',None)

    return Response({"communs": result, "deliveryfees": result_2})
@api_view(['GET'])
def get_cokmmuns(request,pk):
    headers = {"X-API-ID": config.ID_API_YALIDIN,"X-API-TOKEN": config.TOKEN_API_YALIDIN }
    response = requests.get(f"{config.BASE_URL_YALIDIN}communes/?page={pk}", headers=headers)
    communs = response.json()
    result = communs.get('data',None)
    return Response({"communs": result})


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
                    #s = Variation(product=product, category="size", item=size)
                    #s.save()
                    size,create=Size.objects.get_or_create(size=size)
                    for color in colors:
                    #s = Variation(product=product,category="color", item=color)
                    #s.save()
                        color,create=Color.objects.get_or_create(color=color)
                        Variant.objects.create(product=product,size=size,color=color)

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
            url = config.BASE_URL_YALIDIN+"parcels/"
            headers = {"X-API-ID": config.ID_API_YALIDIN,"X-API-TOKEN": config.TOKEN_API_YALIDIN, "Content-Type": "application/json"}
            if not order_obj.edited:
                response = requests.post(url=url, headers=headers, data=json.dumps((data)))
                my_response=response.json()
                transition_yal=my_response[str(order_id)]["tracking"]
                transaction_id=Order.objects.filter(id=order_id).update(transaction_id=transition_yal,confirmed=True)
                print(transaction_id)
                print("yalidin",my_response)
            else:
                data=OrderedDict(
                    [("order_id", str(order_obj.id)), 
                    ("firstname", shipping_obj.name),
                    ("familyname", shipping_obj.name),
                    ("contact_phone",  shipping_obj.phone),
                    ("address", shipping_obj.address),
                    ("to_commune_name", shipping_obj.city),
                    ("to_wilaya_name", shipping_obj.state),
                    ("product_list", str(product_list)),
                    ("price", int(order_obj.get_cart_total)),
                    ("freeshipping", freeshipping), ("is_stopdesk", shipping_obj.is_stopdesk), ("has_exchange", has_exchange), ("product_to_collect", str(product_list))])
                response = requests.patch(url=url+order_obj.transaction_id, headers=headers, data=json.dumps((data)))
                my_response=response.json()
                print("yalidin",my_response)
                order_obj.confirmed=True
                order_obj.save()
                

        else:
            messages.error(request,"le commande n'éxite pas")
    return Response({"success": "true"})

@api_view(['POST'])
def edit_parcel(request):
    if request.method=="POST":
        order=request.data.get("order_tracking",None)
        request.session["order_changed_id"]=order
        print(request.session["order_changed_id"])
    return Response({"success":"true"})
from rest_framework import generics,serializers,filters
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name','description','slug','image']
class ProductList(generics.ListCreateAPIView):
    serializer_class =ProductsSerializer
    search_fields = ['name','description']
    filter_backends = (filters.SearchFilter,)
    queryset = Product.objects.all()

from django.template.loader import render_to_string
import datetime
@api_view(['GET'])
def generate_pdf(request):
    orders_id=request.query_params.get('orders_id').split(',')
    orders_arr= []
    for order in orders_id:
        get_order = Order.objects.filter(id=order).first()
        orders_arr.append(get_order)
    template_path = 'pages/pdf_template.html'
    response = HttpResponse(content_type='application/pdf')
    filename=f'{datetime.date.today()}commande.pdf'
    response['Content-Disposition'] = f'attachment; filename={filename}'
    html = render_to_string(template_path, {'orders_arr': orders_arr})
    pisaStatus = pisa.CreatePDF(html, dest=response)
    return response 