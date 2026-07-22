from . import views
from django.urls import path

urlpatterns = [
    # Authentication
    path("login/", views.staff_login_page, name="staff_login_page"),
    path("login/action", views.staff_login_action, name="staff_login_action"),
    path("logout/", views.staff_logout_action, name="staff_logout_action"),

    # Inventory back office (all gated behind staff_required)
    path("home/", views.home, name="staff_home"),
    path('inventory/', views.inventory, name="staff_inventory"),
    path('inventory/add_items', views.add_items, name='add_items'),
    path('inventory/edit/<int:item_id>', views.edit_item, name='edit_item'),
    path('inventory/handle_inventory_actions', views.handle_inventory_actions, name="handle_inventory_actions"),
]
