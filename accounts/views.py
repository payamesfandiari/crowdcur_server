from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserRegisterForm
from .models import User
from workinterface.models import Job


# Create your views here.

import logging

logger = logging.getLogger(__name__)


class UserRedirectView(LoginRequiredMixin, generic.RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("detail", kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):

    fields = ['username','email','first_name','last_name','age','education','nationality']
    slug_field = "username"
    slug_url_kwarg = "username"

    # we already imported User in the view code above, remember?
    model = User
    # send the user back to their own page after a successful update

    def get_success_url(self):
        return reverse("detail", kwargs={"username": self.request.user.username})

    def get_object(self, **kwargs):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserRegister(generic.CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('work')

    def get_context_data(self, **kwargs):
        context = super(UserRegister,self).get_context_data()
        context['keywords'] = Job.objects.get_keywords()
        return context

    def form_valid(self, form):
        url = super(UserRegister, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = authenticate(username=username,password=password)

        login(self.request,user)
        return url


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = 'accounts/profile.html'
