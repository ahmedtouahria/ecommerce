from django.urls import include, path
from .views import *


urlpatterns = [
    path("cartitemApi/", cartitemApi.as_view(), name="cartitemApi"),
    path("search_products/", search_products, name="search_products"),
    path("product_rating/", rating_product, name="product_rating"),
    path("getcommunstrus/", get_cokmmuns_true, name="get_cokmmuns_true"),
    path("getcommuns/<int:pk>", get_cokmmuns, name="get_communs"),
    path("add_product/", add_product),
    path("send_order/", send_order,name="send_order"),
    path("edit_order/", edit_parcel,name="edite_order"),]
