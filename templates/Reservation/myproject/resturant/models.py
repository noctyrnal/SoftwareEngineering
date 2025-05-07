from django.db import models

from django.db import models

class Reservation(models.Model):
    name = models.CharField(max_length=255, default="John Doe")
    email = models.EmailField(default="example@example.com")
    date = models.DateField(default="2025-01-01")
    time = models.TimeField(default="12:00:00")
    guests = models.IntegerField(default=1)
    
# You can add any other fields that you need, such as customer name, etc.name = models.CharField(max_length=255, default="John Doe")


    # Add any other fields that you need, such as customer name, etc.

    def __str__(self):
        return f"Reservation for {self.date} at {self.time}"
