from django.urls import path, include
from . import views

urlpatterns = [
    path("home/", views.home, name="customer_home"),
    path('products/', views.products, name="customer_products")
]