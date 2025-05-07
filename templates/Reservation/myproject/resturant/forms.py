from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'date', 'time', 'guests']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].widget = forms.TimeInput(attrs={
            'type': 'time',
            'min': '12:00',
            'max': '21:00'
        })

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if date and time:
            exists = Reservation.objects.filter(date=date, time=time).exists()
            if exists:
                raise forms.ValidationError("This time slot is already booked.")
