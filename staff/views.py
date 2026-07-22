from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from .models import Inventory


# The staff back office is gated: a visitor must be authenticated AND flagged
# is_staff. Anyone else (anonymous or a plain customer account) is redirected
# to the staff login page rather than being shown inventory controls.
staff_required = user_passes_test(
    lambda u: u.is_authenticated and u.is_staff,
    login_url='staff_login_page',
)


# --------------------------------------------------------------------------- #
# Authentication
# --------------------------------------------------------------------------- #

def staff_login_page(request):
    # Already a signed-in staff member? Skip the form.
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('staff_inventory')
    return render(request, 'staff/login_page.html')


def staff_login_action(request):
    if request.method != 'POST':
        return redirect('staff_login_page')

    user = authenticate(
        request,
        username=request.POST.get('username'),
        password=request.POST.get('password'),
    )

    if user is None:
        # Deliberately generic: don't reveal which field was wrong.
        messages.error(request, "Invalid username or password.")
        return redirect('staff_login_page')

    if not user.is_staff:
        # Valid credentials, but not a staff account — keep them out.
        messages.error(request, "This account is not authorised for staff access.")
        return redirect('staff_login_page')

    login(request, user)
    messages.success(request, f"Welcome, {user.get_username()}!")
    return redirect('staff_inventory')


def staff_logout_action(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('staff_login_page')


# --------------------------------------------------------------------------- #
# Inventory
# --------------------------------------------------------------------------- #

@staff_required
def home(request):
    return render(request, 'staff/home.html')


@staff_required
def inventory(request):
    all_items = Inventory.objects.all()
    return render(request, 'staff/inventory.html', {"items": all_items})


@staff_required
def add_items(request):
    if request.method == 'POST':
        index = 0
        # The add form submits rows as name_0/price_0/quantity_0, name_1/...
        # Walk them until a name field is missing.
        while True:
            name_key = f'name_{index}'
            if name_key not in request.POST:
                break

            name = request.POST.get(name_key, '').strip()
            try:
                price = Decimal(request.POST.get(f'price_{index}', '').strip())
                quantity = int(request.POST.get(f'quantity_{index}', '').strip())
            except (InvalidOperation, ValueError):
                index += 1
                continue  # skip malformed rows rather than 500

            if name and price >= 0 and quantity >= 0:
                Inventory.objects.create(name=name, price=price, quantity=quantity)
            index += 1

        return redirect('staff_inventory')

    return render(request, 'staff/add_items.html')


@staff_required
def edit_item(request, item_id):
    item = get_object_or_404(Inventory, id=item_id)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        try:
            price = Decimal(request.POST.get('price', '').strip())
            quantity = int(request.POST.get('quantity', '').strip())
        except (InvalidOperation, ValueError):
            messages.error(request, "Price and quantity must be valid numbers.")
            return redirect('edit_item', item_id=item.id)

        if not name:
            messages.error(request, "Name cannot be empty.")
            return redirect('edit_item', item_id=item.id)
        if price < 0 or quantity < 0:
            messages.error(request, "Price and quantity cannot be negative.")
            return redirect('edit_item', item_id=item.id)

        item.name = name
        item.price = price
        item.quantity = quantity
        item.save()
        messages.success(request, f'Updated "{item.name}".')
        return redirect('staff_inventory')

    return render(request, 'staff/edit_item.html', {'item': item})


@staff_required
def handle_inventory_actions(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'resupply':
            # Only add stock where a positive quantity was entered.
            for key, value in request.POST.items():
                if key.startswith('quantity_'):
                    try:
                        item_id = int(key.split('_')[1])
                        added_qty = int(value)
                        if added_qty > 0:
                            item = Inventory.objects.get(id=item_id)
                            item.quantity += added_qty
                            item.save()
                    except (ValueError, Inventory.DoesNotExist):
                        continue

        elif action == 'delete':
            item_ids = request.POST.getlist('items_to_delete')
            if item_ids:
                Inventory.objects.filter(id__in=item_ids).delete()

    return redirect('staff_inventory')
