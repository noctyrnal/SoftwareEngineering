from django.shortcuts import render
from django.utils.timezone import datetime
import json
import os
from datetime import datetime as dt

def staff_scheduling(request, name):
    # Load the placeholder database from the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), 'schedule_data.json')
    with open(json_file_path, 'r') as file:
        schedule_data = json.load(file)

    # Add the day of the week dynamically based on the date
    for entry in schedule_data:
        entry_date = dt.strptime(entry["date"], "%d/%m/%Y")  # Parse the date
        entry["day"] = entry_date.strftime("%A")  # Get the day of the week

    return render(
        request,
        'staff_scheduling/staff_schedule.html', # Request the static staff_schedule.htm file
        {
            'name': name,
            'schedule_data': schedule_data, # Schedule data from schedule_data.json
        }
    )

def schedule_page(request):
    return render(request, 'staff_scheduling/schedule.html')

def time_off_page(request):
    return render(request, 'staff_scheduling/time_off.html')

def request_changes_page(request):
    return render(request, 'staff_scheduling/request_changes.html')

def schedule_management_page(request):
    return render(request, 'staff_scheduling/schedule_management.html')