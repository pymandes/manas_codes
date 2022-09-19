from typing import Optional
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for Manas Codes.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class ContactModel(models.Model):
    name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 150)
    subject = models.CharField(max_length = 200)
    message = models.CharField(max_length = 2000)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self) -> str:
        return self.email
