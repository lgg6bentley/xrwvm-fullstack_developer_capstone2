from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views  # Ensure views is correctly imported

app_name = 'djangoapp'

urlpatterns = [
    path("", views.home, name="home"),  # Ensure this exists
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),  # Only one logout route
    path("register/", views.registration, name="register"),
    path("dealerships/", views.get_dealerships, name="dealerships"),
    path("dealer/<int:dealer_id>/reviews/", views.get_dealer_reviews, name="dealer_reviews"),
    path("dealer/<int:dealer_id>/details/", views.get_dealer_details, name="dealer_details"),
    path("add_review/", views.add_review, name="add_review"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)