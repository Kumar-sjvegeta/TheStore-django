from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def customer_login_page(request):
    return HttpResponse("His this will be the customer login page.")