from django.db import models

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    number_of_guests = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    special_request = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"
