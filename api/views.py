from django.shortcuts import redirect
from rest_framework import viewsets
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from shopping.models import Customer, Order, Product, Rating
from shopping.views import cookieCart
from django.http import JsonResponse
from .serializers import *


class ListUsers(APIView):
    """
    View to list all users in the system.
    """

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.name for user in Customer.objects.all()]
        phones = [user.phone for user in Customer.objects.all()]

        return Response({"usernames": usernames, "phones": phones, })
# in this end point get cart items


def cartitem(request):
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
        print("order", order)
    return cartItem


class cartitemApi(APIView):
    """
    View to number cart item
    """
    def get(self, request, format=None):

        return Response({"cartItem": cartitem(request)})


def validate_username(request):
    username = request.GET.get('username', None)
    phone = request.GET.get('phone', None)
    data = {
        "is_exists": Customer.objects.filter(name=username).exists(),
        "is_number_exists": Customer.objects.filter(phone=phone).exists()

    }
    if data['is_exists']:
        data["error_msg"] = "A user with the username already exists"
    if data['is_number_exists']:
        data["error_msg"] = "A user with the phone already exists"
    return JsonResponse(data)


def search_products(request):
    search_data = request.GET.get('search_data', None)
    products_filtred = Product.objects.filter(name__icontains=search_data)
    data = products_filtred.values()
    return JsonResponse(list(data), safe=False)

def product_rating(request):
    user_id = int(request.data.get('user_id'))
    product_id = int(request.data.get('product_id'))
    stars = int(request.data.get('stars'))
    print(user_id, product_id, stars)
    try:
        user = Customer.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
        print("try")

    except:
        pass
    if stars > 0 and stars < 6:
        rate = Rating.objects.get_or_create(user=user, product=product)
        rate.stars = stars
        rate.save()
    else:
        print("else")
        return JsonResponse({"stars must be enter [0-5]"})
    return JsonResponse({"user": user, "product": product, "stars": stars})


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
                rate = Rating.objects.create(
                    user=user, product=product, stars=stars, content=content)

        except:
            print("except")

        return Response({"message": "Hello, world!"})


@api_view(['GET'])
def get_wilaya(request):
    headers = {"X-API-ID": "99661386291735714432",
               "X-API-TOKEN": "P1S1CFxh3daINmDr7JeTgHikEJiwybB52VyTcB67A5KLkFtSvWRmLfAlnQDNWsbn", 'Accept-Encoding': None, 'Accept': None, }
    response = requests.get(
        "https://api.yalidine.app/v1/wilayas/", headers=headers)
    wilayas = response.json()
    result = wilayas['data']

    return Response(result)


@api_view(['GET'])
def get_cokmmuns_true(request):
    headers = {"X-API-ID": "99661386291735714432",
               "X-API-TOKEN": "P1S1CFxh3daINmDr7JeTgHikEJiwybB52VyTcB67A5KLkFtSvWRmLfAlnQDNWsbn", 'Accept-Encoding': None, 'Accept': None, }
    response = requests.get(
        "https://api.yalidine.app/v1/communes/?has_stop_desk=true", headers=headers)
    response_delevery = requests.get(
        "https://api.yalidine.app/v1/deliveryfees/", headers=headers)
    communs = response.json()
    deliveryfees = response_delevery.json()
    result = communs['data']
    result_2 = deliveryfees['data']

    return Response({"communs": result, "deliveryfees": result_2})


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
            for size in sizes:
                s = Variation(product=product, category="size", item=size)
                s.save()
            for color in colors:
                s = Variation(product=product, category="color", item=color)
                s.save()
            return redirect("index")
        else:
            print("product_ref is NONE")
    return Response({"success": "true"})
