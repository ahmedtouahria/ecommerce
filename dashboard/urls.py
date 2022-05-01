from django.urls import path
from api.views import get_wilaya
from .views import * 
urlpatterns = [
path('',dashboard,name='dashboard'),
path('tables/',tables,name='tables'),
path('add_product/',add_product,name='add_product'),
path('tables/order/<int:pk>',order_detail,name='order_detail'),



]
