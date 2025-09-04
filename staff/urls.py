from . import views
from django.urls import path

urlpatterns = [
    path("home/", views.home, name="staff_home"),
    path('inventory/', views.inventory, name="staff_inventory"),
    path('inventory/add_items', views.add_items, name='add_items'),
    # path('inventory/resupply', views.handle_inventory_actions, name='resupply'),
    # path('inventory/delete_items', views.handle_inventory_actions, name='delete_items')
    path('inventory/handle_inventory_actions', views.handle_inventory_actions, name="handle_inventory_actions")
]