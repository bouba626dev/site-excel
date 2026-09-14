from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("download/<str:filename>", views.download_generated_excel, name="download_generated_excel"),
]
