from django.urls import path
from api.views import get_wilaya
from shopping.views import * 
urlpatterns = [
path('<str:lang>/',index,name='index'),
path('<str:lang>/products/',products,name='products'),
path('<str:lang>/register/',register,name='register'),
path('<str:lang>/login/',login_customer,name='login'),
path('<str:lang>/profile/',profile,name='profile'),
path('<str:lang>/profile/orders',profile_orders,name='profile_orders'),
path('<str:lang>/profile/orders/<str:pk>',myorders,name='myorders'),
path('<str:lang>/products/<str:pk>',product,name='single-product'),
path('<str:lang>/products/<str:pk>/<str:ref_code>',productWithCode,name='single-product-code'),
path('<str:lang>/category=<str:cat>/',categorys,name='category'),
path("logout/", logout_request, name="logout_request"),
path('<str:lang>/cart',card,name='card'),
path('update_item/',updateItem, name="update_item"),
path('process_order/', processOrder),
path('<str:lang>/checkout/success/', success_order, name="success_order"),
path('<str:lang>/checkout',checkout,name='checkout'),
path('<str:lang>/about',about,name='about'),

path('getwilaya',get_wilaya,name='get_wilaya'),

]
