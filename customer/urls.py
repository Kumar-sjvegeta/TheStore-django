from django.urls import path, include
from . import views

urlpatterns = [
    path("home/", views.home, name="customer_home"),
    path('products_json/', views.products_json, name="customer_products_json"),
    path("products/", views.products, name="customer_products"),
    path("products/checkout/", views.checkout, name="customer_checkout")
]