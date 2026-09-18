"""
Paramètres Django du projet.

Les valeurs sensibles (clé secrète, mot de passe BDD) sont lues
depuis le fichier .env à la racine du projet (voir .env.example).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Chemin racine du projet (dossier contenant manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Charge les variables d'environnement depuis .env
load_dotenv(BASE_DIR / ".env")


# --- Sécurité ---

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-dev-only-changez-moi-dans-env",
)

DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

configured_hosts = os.getenv("ALLOWED_HOSTS", "").strip()
platform_host = (
    os.getenv("RENDER_EXTERNAL_HOSTNAME")
    or os.getenv("RAILWAY_PUBLIC_DOMAIN")
    or os.getenv("WEBSITE_HOSTNAME")
)

if configured_hosts:
    ALLOWED_HOSTS = [host.strip() for host in configured_hosts.split(",") if host.strip()]
elif platform_host:
    ALLOWED_HOSTS = [platform_host]
elif DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
else:
    ALLOWED_HOSTS = ["*"]


# --- Applications installées ---

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",  # pages publiques (accueil, etc.)
    "orders",  # commandes et spécifications JSON
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# --- Base de données ---
# DB_ENGINE=sqlite  → développement local sans PostgreSQL (fichier db.sqlite3)
# DB_ENGINE=postgresql → production / quand PostgreSQL est installé (défaut cible)

DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").lower()

if DB_ENGINE == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "site_excel"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# --- Validation des mots de passe ---

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# --- Internationalisation (Guinée) ---

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Africa/Conakry"
USE_I18N = True
USE_TZ = True


# --- Fichiers statiques (CSS, JS, images) ---

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
