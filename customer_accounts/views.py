from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def customer_login_page(request):
    return render(request, 'customer_accounts/login_page.html')