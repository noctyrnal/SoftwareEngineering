from django.urls import path
from . import views

urlpatterns = [
    path('',            views.home,             name='home'),
    path('order/',      views.take_order,       name='take_order'),
    path('orders/',     views.order_list,       name='order_list'),
    path('kitchen/',    views.kitchen_dashboard, name='kitchen_dashboard'),
    path('api/kitchen_orders/', views.kitchen_orders_api, name='kitchen_orders_api'),
]
