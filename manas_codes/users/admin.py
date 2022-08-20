from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from manas_codes.users.forms import UserAdminChangeForm, UserAdminCreationForm
from manas_codes.users.models import ContactModel

User = get_user_model()
AdminSite.site_header = 'ManasCodes Administration'
AdminSite.site_title = 'ManasCodes Admin'


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(ContactModel)
class ContactAdmin(admin.ModelAdmin):

    list_display = ["name", "email", "subject", "message"]
    search_fields = ["name", "email", "subject", "message"]
