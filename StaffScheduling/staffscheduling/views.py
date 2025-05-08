from django.shortcuts import render
from django.utils.timezone import datetime
from django.http import HttpResponseRedirect
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

def time_off_page(request):
    # Path to the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), 'time_off_requests.json')

    if request.method == "POST":
        # Get the submitted data
        time_off_date = request.POST.get("time_off_date")
        reason = request.POST.get("reason")

        # Ensure the data is being captured
        print(f"Date: {time_off_date}, Reason: {reason}")

        # Load existing data from the JSON file
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as file:
                time_off_requests = json.load(file)
        else:
            time_off_requests = []

        # Add the new request to the list
        time_off_requests.append({
            "date": time_off_date,
            "reason": reason
        })

        # Save the updated data back to the JSON file
        with open(json_file_path, 'w') as file:
            json.dump(time_off_requests, file, indent=4)

        # Redirect to the same page after submission
        return HttpResponseRedirect(request.path)

    return render(request, 'staff_scheduling/time_off.html')

def request_changes_page(request):
    # Path to the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), 'requested_changes.json')

    if request.method == "POST":
        # Get the submitted data
        change_date = request.POST.get("change_date")  # Reuse the same field name for date
        reason = request.POST.get("reason")

        # Ensure the data is being captured
        print(f"Date: {change_date}, Reason: {reason}")

        # Load existing data from the JSON file
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as file:
                requested_changes = json.load(file)
        else:
            requested_changes = []

        # Add the new request to the list
        requested_changes.append({
            "date": change_date,
            "reason": reason
        })

        # Save the updated data back to the JSON file
        with open(json_file_path, 'w') as file:
            json.dump(requested_changes, file, indent=4)

        # Redirect to the same page after submission
        return HttpResponseRedirect(request.path)

    return render(request, 'staff_scheduling/request_changes.html')

def schedule_page(request):
    return render(request, 'staff_scheduling/schedule.html')


def schedule_management_page(request):
    return render(request, 'staff_scheduling/schedule_management.html')