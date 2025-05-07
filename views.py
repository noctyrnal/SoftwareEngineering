from django.shortcuts import render, redirect
from .forms import ReservationForm

def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservation_success')
    else:
        form = ReservationForm()
    return render(request, 'reservation.html', {'form': form})

def reservation_success(request):
    return render(request, 'reservation_success.html')
