from django.contrib import admin
from manas_codes.users import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from manas_codes.users.forms import UserAdminChangeForm, UserAdminCreationForm
from myfinance.models import Transaction, Category, Group


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """_summary_

    Args:
        admin (_type_): _description_
    """

    list_display = ["name", "comments", "created", "updated"]
    search_fields = ["name", "comments"]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """_summary_

    Args:
        admin (_type_): _description_
    """

    list_display = ["name", "comments", "created", "updated"]
    search_fields = ["name", "comments"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """_summary_

    Args:
        admin (_type_): _description_
    """

    list_display = ["name", "amount", "paid_for", "paid_by", "paid_to", "date", "category", "comments", "updated", "user"]
    search_fields = ["name", "type", "amount", "paid_for", "paid_by", "paid_to", "category__name", "comments"]
    exclude = ["user"]

    def save_model(self, request, obj, form, change):
        if not change:
            # the object is being created, so set the user
            obj.user = request.user
        obj.save()

