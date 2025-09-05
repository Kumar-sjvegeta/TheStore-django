from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate

# Create your views here.
# superuser - kumar
# password - 12345

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
        user = authenticate(request, username=entered_user, password=entered_pass)
        print(f"type of user --> {type(user)}")
        print(f"user --> {user}")
        if user is None:
            print("invalid credentials")
        else:
            print("Welcome ! ")

        return redirect('customer_login_page')


    return render(request, 'customer_accounts/login_page.html')