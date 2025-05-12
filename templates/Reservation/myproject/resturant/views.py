from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReservationForm
from .models import Reservation
from django.http import JsonResponse



def home(request):
    return render(request, 'index.html')


def reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'reservation.html', {
                'form': ReservationForm(),  # Reset the form after successful submission
                'messages': ['Reservation successful!']
            })
    else:
        form = ReservationForm()

    return render(request, 'reservation.html', {'form': form})
