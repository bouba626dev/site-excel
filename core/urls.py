from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("resultat/", views.generation_result, name="generation_result"),
    path("resultat/confirmer/", views.confirm_payment, name="confirm_payment"),
    path("download/<str:filename>", views.download_generated_excel, name="download_generated_excel"),
]
