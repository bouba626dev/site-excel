from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from .forms import EmailAuthenticationForm, SignUpForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("generation_result")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("generation_result")
    else:
        form = EmailAuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")
