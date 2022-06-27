from django.urls import path
from api.views import get_wilaya
from shopping.views import * 
urlpatterns = [
path('',index,name='index'),
path('products/',products,name='products'),
path('register/',register,name='register'),
path('login/',login_customer,name='login'),
path('profile/',profile,name='profile'),
path('profile/orders',profile_orders,name='profile_orders'),
path('profile/orders/<str:pk>',myorders,name='myorders'),


path('products/<int:pk>',product,name='single-product'),
path('products/<int:pk>/<str:ref_code>',productWithCode,name='single-product-code'),
path("logout/", logout_request, name="logout_request"),
path('card',card,name='card'),
path('update_item/',updateItem, name="update_item"),
path('process_order/', processOrder, name="process_order"),
path('products/checkout',checkout,name='checkout'),
path('getwilaya',get_wilaya,name='get_wilaya'),

]
