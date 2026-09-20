from django.urls import path

from . import views

urlpatterns = [
    path("inscription/", views.signup, name="signup"),
    path("connexion/", views.login_view, name="login"),
    path("deconnexion/", views.logout_view, name="logout"),
]
