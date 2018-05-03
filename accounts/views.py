from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserRegisterForm
from .models import User


# Create your views here.

import logging

logger = logging.getLogger(__name__)


class UserRegister(generic.CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        url = super(UserRegister, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = authenticate(username=username,password=password)

        login(self.request,user)
        return url


class UserDetail(LoginRequiredMixin,generic.DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = 'accounts/profile.html'