from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from staff.models import Inventory
from django.core import serializers
import json
# Create your views here.

def home(request):
    return render(request, 'customer/home.html')

def products(request):
    all_products = Inventory.objects.all()
    return render(request, 'customer/products.html', {"products": all_products})

def products_json(request):
    all_products = Inventory.objects.all()
    print(f"all_products --> {all_products}")
    all_products_serialized = serializers.serialize('json', all_products)
    print(f"all_products_serialized --> {all_products_serialized}")
    json_data = json.loads(all_products_serialized)
    print(f"json_data ---> {json_data}")
    pretty_json_data = json.dumps(json_data, indent=4)
    print(f"pretty_json_data --> {pretty_json_data}")

    return HttpResponse(pretty_json_data, content_type=json)
