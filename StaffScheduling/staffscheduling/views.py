from django.shortcuts import render
import re
from django.utils.timezone import datetime
from django.http import HttpResponse

def staff_scheduling(request, name):
    return render(
        request,
        'staff_scheduling/staff_schedule.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )
