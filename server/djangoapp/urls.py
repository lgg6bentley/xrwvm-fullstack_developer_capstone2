from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.registration, name="register"),

    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    # Dealers and Reviews
    path("dealerships/", views.get_dealerships, name="dealerships"),
    path("dealer/<int:dealer_id>/details/", views.get_dealer_details, name="dealer_details"),
    path("dealer/<int:dealer_id>/reviews/", views.get_dealer_reviews, name="dealer_reviews"),
    path("reviews/dealer/<int:dealer_id>/", views.get_dealer_reviews, name="dealer_reviews_by_id"),

    # Posting Reviews
    path("add_review/", views.post_review, name="add_review"),
    path("submit_review/", views.add_review, name="submit_review"),

    # Optional Dealer Fetch Variants
    path("fetchDealers/", views.fetch_dealers, name="fetch_dealers"),
    path("fetchDealer/<int:dealer_id>/", views.fetch_dealer_by_id, name="fetch_dealer_by_id"),
    path("fetchDealers/<str:state>/", views.fetch_dealers_by_state, name="fetch_dealers_by_state"),
    path("dealers/grid/", views.fetch_dealers, name="dealer-grid"),

    path("get_dealers/", views.get_dealerships, name="get_dealers"),
    path("get_dealers/<str:state>/", views.get_dealerships, name="get_dealers_by_state"),

    # Cars
    path("cars/", views.get_cars, name="get_cars"),
    path("api/cars/", views.get_cars, name="api_cars"),

    # Session & user info
    path("user_status/", views.user_status, name="user_status"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)