from datetime import datetime, timedelta, time
from django import forms
from django.core.exceptions import ValidationError
from .models import Reservation

def round_up_to_next_15_min(dt):
    minute = (dt.minute // 15 + 1) * 15
    if minute == 60:
        dt += timedelta(hours=1)
        minute = 0
    return dt.replace(minute=minute, second=0, microsecond=0)

def generate_time_choices():
    now = datetime.now()
    start = round_up_to_next_15_min(now)
    end = datetime.combine(now.date(), time(20, 0))  # closing buffer: 8:00 PM

    choices = []
    current = start
    while current <= end:
        formatted = current.strftime("%H:%M")
        choices.append((formatted, formatted))
        current += timedelta(minutes=15)
    return choices

class ReservationForm(forms.ModelForm):
    time = forms.ChoiceField(choices=generate_time_choices())

    class Meta:
        model = Reservation
        fields = ['name', 'email', 'date', 'time', 'guests']

    def clean_time(self):
        time_str = self.cleaned_data['time']
        return datetime.strptime(time_str, "%H:%M").time()

    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        email = cleaned_data.get('email')
        guests = cleaned_data.get('guests')

        if not (date and time and email and guests):
            return

        # Limit max guests per reservation
        if guests > 5:
            raise forms.ValidationError("You can only book up to 5 guests per reservation.")

        # Prevent double booking by same email
        if Reservation.objects.filter(date=date, time=time, email=email).exists():
            raise forms.ValidationError("You already have a reservation at this time.")

        # Limit total guests per hour (e.g. 20 guests max per hour)
        hour_start = time.replace(minute=0)
        hour_end = (datetime.combine(date, hour_start) + timedelta(hours=1)).time()

        existing_reservations = Reservation.objects.filter(
            date=date,
            time__gte=hour_start,
            time__lt=hour_end
        )

        total_guests = sum(r.guests for r in existing_reservations)
        if total_guests + guests > 20:
            raise forms.ValidationError("Too many guests booked for this hour. Try another time.")
