from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def customer_login_page(request):
    # Already signed in? Send them straight to the store.
    if request.user.is_authenticated:
        return redirect('customer_products')
    return render(request, 'customer_accounts/login_page.html')


def customer_login_action(request):
    # Only POST carries credentials; anything else just shows the form.
    if request.method != 'POST':
        return redirect('customer_login_page')

    entered_user = request.POST.get('username')
    entered_pass = request.POST.get('password')
    user = authenticate(request, username=entered_user, password=entered_pass)

    if user is None:
        # Deliberately vague so we don't reveal which field was wrong.
        messages.error(request, "Invalid username or password.")
        return redirect('customer_login_page')

    # Valid credentials: establish the session and land on the store.
    login(request, user)
    messages.success(request, f"Welcome, {user.get_username()}!")
    return redirect('customer_products')


def customer_logout_action(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('customer_login_page')
