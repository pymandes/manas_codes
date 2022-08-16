import email
from email import message
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.http import HttpResponseRedirect

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()

def HomepageView(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            print('Saving message')
            message = 'Message sent!!'
            return render(request, "pages/index.html", {'form': form, 'message': message})

    form = ContactForm()
    return render(request, "pages/index.html", {'form': form})


def contact(request):

    print('contact')

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            print('Saving message')
            message = 'Message sent!!'
            return HttpResponseRedirect('index', {'message': message})
