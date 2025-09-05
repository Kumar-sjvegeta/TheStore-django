from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def customer_login_page(request):
    return render(request, 'customer_accounts/login_page.html')

def customer_login_action(request):
    print(f"request.method ---> {request.method}")
    if request.method == 'POST':
        print(f"request.POST ---> {request.POST}")
        entered_user = request.POST.get('username')
        entered_pass = request.POST.get('password')
        print(f"Entered username --> {entered_user}")
        print(f"Entered password --> {entered_pass}")

        return redirect('customer_login_page')


    return render(request, 'customer_accounts/login_page.html')