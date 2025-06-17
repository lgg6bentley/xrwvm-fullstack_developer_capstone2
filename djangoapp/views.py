from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Login request view (Handles both JSON and form-based requests)
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                username = data.get("username")  # Standardized variable name
                password = data.get("password")
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
        else:
            username = request.POST.get("username")  # Handles form POST request
            password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:home")  # Redirect to homepage with namespace
        return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")  # Show login page on GET request

# Logout request view (Clears session and redirects)
def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("djangoapp:home")  # Fixed namespace reference

# User registration view (Handles JSON-based registration)
@csrf_exempt
def registration(request):
    if request.method == "POST":
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                username = data.get("username")
                password = data.get("password")
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")

        if username and password:
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already taken"}, status=400)
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return JsonResponse({"message": "User registered successfully!", "username": username})
        return JsonResponse({"error": "Invalid registration data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)

# About Page View
def about(request):
    return render(request, "about.html")

# Contact Page View
def contact(request):
    return render(request, "contact.html")

# Home Page View (Renders the home page)
def home(request):
    return render(request, "home.html")

# Login Page View (Renders HTML form login)
def login_page(request):
    return render(request, "login.html")

# Get dealerships view
def get_dealerships(request):
    return render(request, "dealerships.html")

# Get dealer reviews view
def get_dealer_reviews(request, dealer_id):
    context = {"dealer_id": dealer_id}
    return render(request, "dealer_reviews.html", context)

# Get dealer details view
def get_dealer_details(request, dealer_id):
    context = {"dealer_id": dealer_id}
    return render(request, "dealer_details.html", context)

# Add review view (Handles JSON submission)
@csrf_exempt
def add_review(request):
    if request.method == "POST":
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                review_text = data.get("review")
                dealer_id = data.get("dealer_id")
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
        else:
            review_text = request.POST.get("review")
            dealer_id = request.POST.get("dealer_id")

        if review_text and dealer_id:
            return JsonResponse({"message": "Review submitted!", "dealer_id": dealer_id})
        return JsonResponse({"error": "Incomplete review data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)