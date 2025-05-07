from django.urls import path
from . import views

urlpatterns = [
    path('', views.make_reservation, name='make_reservation'),
    path('reserved-slots/', views.get_reserved_slots, name='reserved_slots'),
]
