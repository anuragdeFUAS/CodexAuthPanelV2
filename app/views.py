from __future__ import annotations
from typing import Union

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from rest_framework.request import Request

from django.core.mail import send_mail

from .forms import UserRegisterForm, ProfileUpdateForm
# from .forms import UserRegisterForm, UserProfile, ProfileUpdateForm


# Lets structure it when are making a viewfirst handle the GET request and then the POST request
# Also when we are replying to a request instead of putting in dictionary made inside return redirect put a context
#


def home(request):
    return redirect("app:login")


def register(request: Request) -> Union[render, redirect]:
    """
    This view handles both GET and POST requests for user registration. If the request is GET, it renders the
    registration form. If the request is POST, it validates the form and creates a new user. If the form is valid, it
    creates a new user, creates a token for the user, creates a user profile, and redirects the user to the login page.
    If the form is invalid, it renders the registration form again with the error message.
    """
    if request.method == "GET":
        context = {
            "form": UserRegisterForm(),
        }
        return render(request, "register.html", context)
    elif request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create and associate a token with the user
            token, created = Token.objects.get_or_create(user=user)

            user_fullname = user.first_name + " " + user.last_name
            welcome_message = "Hi " + user_fullname + "! Thank you for registering with us."
            
            # After the new user is created, send an email
            send_mail(
                'Welcome to our website',
                welcome_message,
                'authcodex@gmail.com',
                [user.email],
                fail_silently=False,
            )

            # form.cleaned_data.get('username')
            messages.success(request, "Your account has been created! You are now able to log in")
            return redirect("app:login")
        else:
            # error = form.errors.get() #Error is not comming exactly
            context = {
                "form": form,
                # 'error': error,
            }
            # form = UserRegisterForm()
            return render(request, "register.html", context)


@login_required
def profile(request: Request) -> render:
    """
    This view handles both GET and POST requests for user profile. If the request is GET, it renders the profile page.
    If the request is POST, it validates the form and updates the user profile. If the form is valid, it updates the
    user profile and redirects the user to the profile page. If the form is invalid, it renders the profile page again
    with the error message.
    """
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("app:profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {"form": form, 'title': 'Profile'}
    return render(request, "profile.html", context)

