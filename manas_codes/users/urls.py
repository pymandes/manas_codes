from django.urls import path

from manas_codes.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    add_contact
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("add_contact/", view=add_contact, name="add-contact"),
]
