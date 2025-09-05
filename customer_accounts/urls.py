from django.urls import path
from . import views

urlpatterns = [
    path("customer_login/", views.customer_login_page, name='customer_login_page')
]