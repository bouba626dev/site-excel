"""
URLs principales du projet.

Les URLs de l'app core (page d'accueil) sont incluses à la racine (/).
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]
