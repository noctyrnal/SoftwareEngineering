from django.urls import path
from . import views

urlpatterns = [
    path('reserve/', views.make_reservation, name='make_reservation'),
    path('reserve/success/', views.reservation_success, name='reservation_success'),
]
