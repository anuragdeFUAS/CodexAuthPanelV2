import re

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    """'
    This is the class for Registration Form
    """
    username = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=200, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    

    class Meta:
        model = UserProfile
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def clean_password2(self):
        # Clean the password fields once more
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        # Check if the password fields match
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")

        # Check the length of the password
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        # Check if password contains a micture of letters and numbers
        if not re.search(r"\d", password1) or not re.search(r"[a-zA-Z]", password1):
            raise ValidationError("Password must contain a mixture of letters and numbers")

        return password2


class ProfileUpdateForm(forms.ModelForm):

    email = forms.EmailField(max_length=200, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=50, required=False)
    state = forms.CharField(max_length=50, required=False)
    zip = forms.CharField(max_length=50, required=False)
    country = forms.CharField(max_length=50, required=False)
    
    class Meta:
        model = UserProfile
        fields = [
            "email", "first_name", "last_name", "phone", "address", "city", "state", "zip", "country"
        ]
