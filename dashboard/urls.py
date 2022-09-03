from django.urls import path
from .views import * 
urlpatterns = [
path('',dashboard,name='dashboard'),
path('commandes/',tables,name='tables'),
path('stock/',stock,name='stock'),
path('stock/<int:pk>',single_product,name='single_product'),
path('add_product/',add_product,name='add_product'),
path('options/',options,name='options'),
path('commandes/order/<str:pk>',order_detail,name='order_detail'),
]
