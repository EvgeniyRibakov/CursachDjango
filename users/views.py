# users/views.py
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
)
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterView(CreateView):
    model = CustomUser
    form_class = UserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("login")


class LoginView(BaseLoginView):
    template_name = "login.html"


class LogoutView(BaseLogoutView):
    next_page = reverse_lazy("login")
