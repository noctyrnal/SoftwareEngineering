from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import date

class Reservation(models.Model):
    name = models.CharField(max_length=100, default='John Doe')  # Example: 'John Doe'
    email = models.EmailField(default='example@example.com')  # Example: 'example@example.com'
    date = models.DateField(default=date.today())  # Example: today's date
    time = models.TimeField(default='19:00')  # Example: '19:00' (7:00 PM)
    guests = models.IntegerField(default=2)  # Example: 2 guests

    def __str__(self):
        return f"Reservation for {self.name} on {self.date} at {self.time} for {self.guests} guests"
