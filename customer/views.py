from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from staff.models import Inventory
# Create your views here.

def home(request):
    return render(request, 'home.html')

def products(request):
    all_products = Inventory.objects.all()
    return HttpResponse(all_products)