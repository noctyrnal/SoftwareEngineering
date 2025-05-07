from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
@login_required
def home(request):
    """
    Post-login landing page: choose between taking a new order
    or viewing the kitchen dashboard.
    """
    return render(request, 'pos/home.html')
