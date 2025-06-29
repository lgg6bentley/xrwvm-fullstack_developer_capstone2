from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from pymongo import MongoClient
import logging
import json

logger = logging.getLogger(__name__)

# ✅ Session/User Status
@login_required(login_url='/login/')
def user_status(request):
    return JsonResponse({
        "logged_in": True,
        "username": request.user.username,
        "is_superuser": request.user.is_superuser
    })


# ✅ Static pages
def home(request):
    return render(request, 'Home.html')

def about(request):
    return render(request, "About.html")

def contact(request):
    return render(request, "Contact.html")


# ✅ Registration/Login/Logout
def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("djangoapp:home")
    else:
        form = UserCreationForm()
    return render(request, "registration.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("djangoapp:home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")

def login_page(request):
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect("djangoapp:home")


# ✅ Dealer Views (MongoDB)
def get_dealerships(request):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["dealerships"]
        dealers = list(db["dealers"].find({}, {"_id": 0}))

        formatted = [{
            "id": d.get("dealer_id", 0),
            "name": d.get("full_name", ""),
            "city": d.get("city", ""),
            "state": d.get("state", ""),
            "address": d.get("address", ""),
            "zip": d.get("zip", "")
        } for d in dealers]

        return JsonResponse({"dealerships": formatted})
    except Exception as e:
        logger.exception("Failed to fetch dealerships")
        return JsonResponse({"status": 500, "error": "Unable to retrieve dealerships"})


def fetch_dealer_by_id(request, dealer_id):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["dealerships"]
        dealer = db["dealers"].find_one({"dealer_id": dealer_id}, {"_id": 0})
        if dealer:
            return JsonResponse({"dealer": dealer})
        else:
            return JsonResponse({"status": 404, "error": "Dealer not found"})
    except Exception as e:
        logger.exception("Error fetching dealer by ID")
        return JsonResponse({"status": 500, "error": "Server error"})


def get_dealer_details(request, dealer_id):
    return fetch_dealer_by_id(request, dealer_id)


def fetch_dealers_by_state(request, state):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["dealerships"]
        dealers = list(db["dealers"].find({"state": state}, {"_id": 0}))
        if dealers:
            return JsonResponse({"dealers": dealers})
        else:
            return JsonResponse({"status": 404, "error": f"No dealers found in {state}"})
    except Exception as e:
        logger.exception("Error fetching dealers by state")
        return JsonResponse({"status": 500, "error": "Server error"})


def fetch_dealers(request):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["dealerships"]
        dealers = list(db["dealers"].find({}, {"_id": 0}))
        for dealer in dealers:
            dealer["_id"] = str(dealer.get("_id", ""))
        return render(request, 'dealer_grid.html', {"dealers": dealers})
    except Exception as e:
        logger.exception("Error fetching dealers for grid")
        return JsonResponse({"status": 500, "error": "Server error fetching dealers"})


# ✅ Cars
def get_cars(request):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["dealerships"]
        cars = list(db["cars"].find({}, {"_id": 0}))
        return JsonResponse({"cars": cars})
    except Exception as e:
        logger.exception("Error fetching cars")
        return JsonResponse({"status": 500, "error": "Server error"})


# ✅ Reviews
@csrf_exempt
@login_required(login_url='/login/')
def post_review(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            dealer_id = data.get("dealer_id")
            review_text = data.get("review")
            rating = data.get("rating")

            client = MongoClient("mongodb://localhost:27017/")
            db = client["dealerships"]
            db["reviews"].insert_one({
                "dealer_id": dealer_id,
                "review": review_text,
                "rating": rating,
                "user": request.user.username
            })

            return JsonResponse({"status": 200, "message": "Review submitted!"})
        except Exception as e:
            logger.exception("Failed to submit review")
            return JsonResponse({"status": 500, "error": "Server error during review submission"})

    return JsonResponse({"status": 405, "error": "Only POST method allowed"})


def get_dealer_reviews(request, dealer_id):
    # Placeholder – plug in real review logic if needed
    return JsonResponse({
        "dealer_id": dealer_id,
        "reviews": [
            {"user": "admin", "rating": 5, "comment": "Excellent service!"},
            {"user": "guest", "rating": 4, "comment": "Smooth experience."}
        ]
    })


@login_required(login_url='/login/')
def add_review(request):
    return render(request, "add_review.html")