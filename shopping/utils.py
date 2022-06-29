import uuid
import json
from .models import *
'''
We need generate a random code for any user to subscribe
'''
def generate_random_code():
    code = str(uuid.uuid4()).replace('-', '')[:12]
    return code
def generate_transform_id():
    code = str(uuid.uuid4()).replace('-', '')[:8]
    return code

''' cookieData=cookieCart(request)
        items=cookieData['items']
        order=cookieData['order']
        cartItem=cookieData['cartItem'] '''

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
