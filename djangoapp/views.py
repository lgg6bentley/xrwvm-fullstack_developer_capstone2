from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .models import CarMake, CarModel
from .utils import initiate
from .restapis import get_request, analyze_review_sentiments
from rest_framework import viewsets
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
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

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:home")
        return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("djangoapp:home")

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

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def home(request):
    return render(request, "home.html")

def login_page(request):
    return render(request, "login.html")

def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state.lower() == "all" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships if dealerships else []})

def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        if reviews:
            for review_detail in reviews:
                response = analyze_review_sentiments(review_detail.get('review', ''))
                print(response)
                review_detail['sentiment'] = response.get('sentiment', 'unknown')

        return JsonResponse({"status": 200, "reviews": reviews if reviews else []})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

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

def get_cars(request):
    count = CarMake.objects.count()
    print(f"CarMake count: {count}")

    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('carmake')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.carmake.name
        })

    return JsonResponse({"CarModels": cars})

def fetch_dealers(request):
    dealers = [
        {"id": 1, "name": "Kansas Auto Group", "state": "KS"},
        {"id": 2, "name": "Topeka Imports", "state": "KS"},
        {"id": 3, "name": "Maple Street Motors", "state": "NY"},
    ]
    return JsonResponse(dealers, safe=False)

def fetch_dealer_by_id(request, dealer_id):
    dealer = {
        "id": dealer_id,
        "name": f"Dealer #{dealer_id}",
        "state": "KS" if dealer_id == 1 else "Unknown",
        "address": "123 Main St",
        "city": "Topeka",
    }
    return JsonResponse(dealer)

def fetch_dealers_by_state(request, state):
    filtered = [
        {"id": 1, "name": "Kansas Auto Group", "state": "KS"},
        {"id": 2, "name": "Topeka Imports", "state": "KS"},
    ] if state.lower() == "kansas" else []
    return JsonResponse(filtered, safe=False)

def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})