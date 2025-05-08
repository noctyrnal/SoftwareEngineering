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
        # Parse the date in d/m/y format
        entry_date = dt.strptime(entry["date"], "%d/%m/%Y")
        entry["day"] = entry_date.strftime("%A")  # Get the day of the week

    return render(
        request,
        'staff_scheduling/staff_schedule.html',
        {
            'name': name,
            'schedule_data': schedule_data,
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

def schedule_management_page(request):
    # Path to the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), 'schedule_data.json')

    # Load existing data from the JSON file
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            schedule_data = json.load(file)
    else:
        schedule_data = []

    if request.method == "POST":
        # Check if the "Log in" button was pressed
        if "login" in request.POST:
            # Handle the login logic here (if needed)
            print("Log in button pressed")
            return HttpResponseRedirect(request.path)

        # Check if the "Update" button was pressed
        if "update" in request.POST:
            # Get the row index to update
            row_index = int(request.POST.get("update")) - 1

            # Get the updated date and time
            updated_date = request.POST.get("date")
            updated_time = request.POST.get("time")

            # Ensure the date is saved in d/m/y format
            parsed_date = dt.strptime(updated_date, "%Y-%m-%d").strftime("%d/%m/%Y")

            # Update the corresponding entry in the schedule data
            schedule_data[row_index]["date"] = parsed_date
            schedule_data[row_index]["time"] = updated_time

            # Save the updated data back to the JSON file
            with open(json_file_path, 'w') as file:
                json.dump(schedule_data, file, indent=4)

            # Redirect to the same page after submission
            return HttpResponseRedirect(request.path)

    return render(request, 'staff_scheduling/schedule_management.html', {
        'schedule_data': schedule_data
    })

def inventory_page(request):
    # Path to the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), 'inventory.json')

    # Load existing data from the JSON file
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            inventory_data = json.load(file)
    else:
        inventory_data = []

    return render(request, 'staff_scheduling/inventory.html', {
        'inventory_data': inventory_data
    })

def resupply_page(request):
    # Path to the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), 'inventory.json')

    # Load existing data from the JSON file
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            inventory_data = json.load(file)
    else:
        inventory_data = []

    if request.method == "POST":
        # Get the submitted data
        item_name = request.POST.get("item")
        quantity = int(request.POST.get("quantity"))
        restock_level = int(request.POST.get("restock_level"))
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")

        # Check if the item already exists in the inventory
        item_found = False
        for item in inventory_data:
            if item["item"].lower() == item_name.lower():
                # Update the existing item
                item["quantity"] = quantity
                item["restock_level"] = restock_level
                item["phone_number"] = phone_number
                item["email"] = email
                item_found = True
                break

        if not item_found:
            # Add a new item to the inventory
            inventory_data.append({
                "item": item_name,
                "quantity": quantity,
                "restock_level": restock_level,
                "phone_number": phone_number,
                "email": email
            })

        # Save the updated data back to the JSON file
        with open(json_file_path, 'w') as file:
            json.dump(inventory_data, file, indent=4)

        # Redirect to the inventory page after submission
        return HttpResponseRedirect('/inventory/')

    return render(request, 'staff_scheduling/resupply.html', {
        'inventory_data': inventory_data
    })