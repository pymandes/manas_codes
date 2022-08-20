from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from manas_codes.users.forms import UserAdminChangeForm, UserAdminCreationForm
from myexpenses.models import Transaction, Category, Group


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ["name", "comments", "created"]
    search_fields = ["name", "comments"]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):

    list_display = ["name", "comments", "created"]
    search_fields = ["name", "comments"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = ["name", "type", "amount", "paid_for", "paid_by", "paid_to", "date", "category"]
    search_fields = ["name", "type", "amount", "paid_for", "paid_by", "paid_to", "category__name"]

