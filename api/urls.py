from django.urls import include, path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('category',CategoryViewSet)
urlpatterns = [
    path("listusersapi/", ListUsers.as_view(), name="listusersapi"),
    path("cartitemApi/", cartitemApi.as_view(), name="cartitemApi"),
    path("validate_username/", validate_username, name="validate_username"),
    path("search_products/", search_products, name="search_products"),
    path("product_rating/", rating_product, name="product_rating"),
    path("getcommunstrus/", get_cokmmuns_true, name="get_cokmmuns_true"),
    path("add_product/", add_product),
    
    
    
    path('', include(router.urls)),
]
