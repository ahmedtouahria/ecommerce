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

