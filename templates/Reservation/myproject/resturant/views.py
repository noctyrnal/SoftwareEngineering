from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReservationForm
from .models import Reservation
from django.http import JsonResponse

def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Reservation successful!")
            return redirect('make_reservation')  # Make sure your URL name matches this
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ReservationForm()

    return render(request, 'reservation.html', {'form': form})

def get_reserved_slots(request):
    reservations = Reservation.objects.all().values('date', 'time')
    return JsonResponse(list(reservations), safe=False)
