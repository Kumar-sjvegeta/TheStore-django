from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Inventory

# Create your views here.

def home(request):
    return render(request, 'home.html')

def inventory(request):
    all_items = Inventory.objects.all()
    return render(request, 'inventory.html', {"items": all_items})

def resupply(request):
    if request.method == 'POST':
    # Iterate through all items and update their quantities
        print(f"request.post ---> {request.POST}")
        for item in Inventory.objects.all():
            key = f'quantity_{item.id}'
            if key in request.POST and request.POST[key]:
                try:
                    added_qty = int(request.POST[key])
                    if added_qty > 0:
                        item.quantity = item.quantity + added_qty
                        item.save()
                except ValueError:
                    pass # skipping if non-integer value is submitted.
    return redirect('staff_inventory')

# def add_items(request):
#     if request.method == 'POST':
#         i = 0
#         while True:
#             name_key = f'name_{i}'
#             price_key = f'price_{i}'
#             quantity_key = f'quantity_{i}'
#
#             if name_key not in request.POST:
#                 break
#                 #no more records
#             name = request.POST.get(name_key, '').strip()
#             try:
#                 price = float(request.POST.get(price_key, '0'))
#                 quantity = int(request.POST.get(quantity_key, '0'))
#             except ValueError:
#                 i += 1
#                 continue #skipping invalid row
#
#             if name and price >= 0 and quantity >= 0:
#                 Inventory.objects.create(name=name, price=price, quantity=quantity)
#
#             i += 1
#
#         return redirect('staff_inventory')
#     return render(request, 'add_items.html')


# def add_items(request):
#     if request.method == 'POST':
#         i = 0
#         while True:
#             name_key = f'name_{i}'
#             price_key = f'price_{i}'
#             quantity_key = f'quantity_{i}'
#
#             if name_key not in request.POST:
#                 break  # No more rows
#
#             name = request.POST.get(name_key, '').strip()
#             price = request.POST.get(price_key, '').strip()
#             quantity = request.POST.get(quantity_key, '').strip()
#
#             if name:  # Only process rows where name is filled
#                 try:
#                     price = float(price)
#                     quantity = int(quantity)
#                     if price >= 0 and quantity >= 0:
#                         Inventory.objects.create(name=name, price=price, quantity=quantity)
#                 except ValueError:
#                     pass  # Skip invalid rows silently
#
#             i += 1
#
#         return redirect('staff_inventory')
#
#     return render(request, 'add_items.html')

def add_items(request):
    if request.method == 'POST':
        print(request.POST)
        index = 0
        while True:
            print("Entered while loop. about to get keys")
            name_key = f'name_{index}'
            price_key = f'price_{index}'
            quantity_key = f'quantity_{index}'
            print("after getting the keys. printing them")
            print(f"name key --> {name_key}")
            print(f"price key --> {price_key}")
            print(f"quantity_key key --> {quantity_key}")

            # Break when no more name fields are found
            if name_key not in request.POST:
                break

            name = request.POST.get(name_key, '').strip()
            price = float(request.POST.get(price_key, '').strip())
            quantity = int(request.POST.get(quantity_key, '').strip())
            print(f"Product details: ")
            print(f"Name : {name}, Price: {price}, Quantity: {quantity}")

            # Only save if name and both numeric fields are valid
            if name and price >= 0 and quantity >= 0:
                print("Enterd the for loop to create new items")
                try:
                    price = float(price)
                    quantity = int(quantity)
                    if price >= 0 and quantity >= 0:
                        Inventory.objects.create(name=name, price=price, quantity=quantity)
                except ValueError:
                    # Skip invalid rows silently
                    pass

            index += 1

        return redirect('staff_inventory')

    return render(request, 'add_items.html')

def delete_items(request):
    if request.method == 'POST':
        item_ids = request.POST.getlist('items_to_delete')
        #getlist retrieves a list of all values for the specified key - here - items_to_delete
        #the key is always the name attribute and the name attribute of our shechboxes is items_to_delete
        if item_ids:
            Inventory.objects.filter(id__in=item_ids).delete()
    return redirect('staff_inventory')


# def handle_inventory_actions(request):
#     print(f"request method --> {request.method}")
#     print(f"request data --> {request.POST}")
#     if request.method == 'POST':
#         action = request.POST.get('action')
#
#         if action == 'resupply':
#             # This is the corrected loop to prevent unintended updates
#             for key, value in request.POST.items():
#                 if key.startswith('quantity_') and value.isdigit():
#                     try:
#                         item_id = int(key.split('_')[1])
#                         added_qty = int(value)
#
#                         if added_qty > 0:
#                             item = Inventory.objects.get(id=item_id)
#                             item.quantity += added_qty
#                             item.save()
#                     except (ValueError, Inventory.DoesNotExist):
#                         continue  # Skip to the next item if an error occurs
#
#         elif action == 'delete':
#             item_ids = request.POST.getlist('items_to_delete')
#             if item_ids:
#                 Inventory.objects.filter(id__in=item_ids).delete()
#             # Optionally, add a success message here
#
#         return redirect('staff_inventory')  # Redirect back to the inventory page
#
#     # This part handles the GET request to display the page
#     items = Inventory.objects.all()
#     context = {
#         'items': items
#     }
#     return render(request, 'inventory.html', context)

def handle_inventory_actions(request):
    print(f"request method --> {request.method}")
    print(f"request data --> {request.POST}")
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'resupply':
            # This is the corrected loop to prevent unintended updates
            for key, value in request.POST.items():
                if key.startswith('quantity_'):
                    try:
                        item_id = int(key.split('_')[1])
                        added_qty = int(value)

                        # Only update if the submitted quantity is greater than 0
                        if added_qty > 0:
                            item = Inventory.objects.get(id=item_id)
                            item.quantity += added_qty
                            item.save()
                    except (ValueError, Inventory.DoesNotExist):
                        continue  # Skip to the next item if an error occurs

        elif action == 'delete':
            item_ids = request.POST.getlist('items_to_delete')
            if item_ids:
                Inventory.objects.filter(id__in=item_ids).delete()
            # Optionally, add a success message here

        return redirect('staff_inventory')  # Redirect back to the inventory page

    # This part handles the GET request to display the page
    items = Inventory.objects.all()
    context = {
        'items': items
    }
    return render(request, 'inventory.html', context)