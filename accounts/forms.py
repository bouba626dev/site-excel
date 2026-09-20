from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")
        labels = {
            "email": "Adresse email",
            "password1": "Mot de passe",
            "password2": "Confirmer le mot de passe",
        }


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Adresse email")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            self.user = authenticate(email=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Email ou mot de passe incorrect.")
        return cleaned_data
