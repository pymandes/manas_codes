from django.contrib import admin, messages
from manas_codes.users import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.shortcuts import HttpResponse, render, redirect
import logging
import csv
from io import StringIO, TextIOWrapper
from django.urls import path
import uuid

from myfinance.models import Transaction, Category, Group
from myfinance.forms import CsvImportForm


class ExportCsvMixin:
    """_summary_"""

    @admin.action(description="Export selected records to CSV")
    def export_as_csv(self, request, queryset):
        """_summary_

        Args:
            request (_type_): _description_
            queryset (_type_): _description_

        Returns:
            _type_: _description_
        """
        logging.debug(f"Loading ExportCsvMixin for {request.user.name}")
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin, ExportCsvMixin):
    """_summary_

    Args:
        admin (_type_): _description_
    """

    list_display = ["name", "comments", "created", "updated"]
    search_fields = ["name", "comments"]
    actions = ["export_as_csv"]

    change_list_template = "myfinance/category/category_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        logging.debug(f"Loading category import_csv for {request.user.name}")
        if request.method == "POST":
            with TextIOWrapper(request.FILES["csv_file"], encoding="utf-8") as csv_file:
                logging.debug(f"CSV File added: {csv_file}")
                file_name = csv_file.name
                if not file_name.endswith(".csv"):
                    logging.warn(f"Invalid file type imported {file_name}")
                    messages.error(
                        request,
                        "Invalid file type selected, please upload right CSV file",
                    )
                    return redirect("..")
                reader = csv.DictReader(csv_file)

                record_created = 0

                for row in reader:
                    logging.debug(f"Row loaded from reader: {row}")
                    name = row["name"]
                    comments = row["comments"]
                    createdDate = row["created"]
                    updatedDate = row["updated"]

                    logging.debug(f"Line read for {name}")
                    category, created = Category.objects.update_or_create(
                        name=name,
                        comments=comments,
                        created=createdDate,
                        updated=updatedDate,
                    )

                    if created:
                        record_created = record_created + 1

                    logging.debug(
                        f"Record with category {category} has been created"
                        if created
                        else f"Record with category {category} ignored."
                    )
                message = f"Csv file: {file_name} has been imported for {record_created} records."
                logging.info(message)
                self.message_user(request, message)
            return redirect("..")

        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "myfinance/csv_form.html", payload)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin, ExportCsvMixin):
    """_summary_

    Args:
        admin (_type_): _description_
    """

    list_display = ["name", "comments", "created", "updated"]
    search_fields = ["name", "comments"]
    actions = ["export_as_csv"]

    change_list_template = "myfinance/group/group_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        logging.debug(f"Loading group import_csv for {request.user.name}")
        if request.method == "POST":
            with TextIOWrapper(request.FILES["csv_file"], encoding="utf-8") as csv_file:
                logging.debug(f"CSV File added: {csv_file}")
                file_name = csv_file.name
                if not file_name.endswith(".csv"):
                    logging.warn(f"Invalid file type imported {file_name}")
                    messages.error(
                        request,
                        "Invalid file type selected, please upload right CSV file",
                    )
                    return redirect("..")
                reader = csv.DictReader(csv_file)

                record_created = 0

                for row in reader:
                    logging.debug(f"Row loaded from reader: {row}")
                    name = row["name"]
                    comments = row["comments"]
                    createdDate = row["created"]
                    updatedDate = row["updated"]

                    logging.debug(f"Line read for {name}, {createdDate}")
                    group, group_created = Group.objects.update_or_create(
                        name=name,
                        comments=comments,
                        created=createdDate,
                        updated=updatedDate,
                    )

                    if group_created:
                        record_created = record_created + 1

                    logging.debug(
                        f"Record with group {group} has been created"
                        if group_created
                        else f"Record with group {group} ignored."
                    )
                message = f"Csv file: {file_name} has been imported for {record_created} records."
                logging.info(message)
                self.message_user(request, message)
            return redirect("..")

        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "myfinance/csv_form.html", payload)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin, ExportCsvMixin):
    """_summary_

    Args:
        admin (_type_): _description_
    """

    list_display = [
        "name",
        "amount",
        "paid_for",
        "paid_by",
        "paid_to",
        "date",
        "category",
        "group",
        "comments",
        "created",
        "updated",
        "user",
    ]
    search_fields = [
        "name",
        "type",
        "amount",
        "paid_for",
        "paid_by",
        "paid_to",
        "category__name",
        "comments",
    ]
    # exclude = ["user"]
    actions = ["export_as_csv"]

    change_list_template = "myfinance/transaction/transaction_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        logging.debug(f"Loading transaction import_csv for {request.user.name}")
        if request.method == "POST":
            with TextIOWrapper(request.FILES["csv_file"], encoding="utf-8") as csv_file:
                logging.debug(f"CSV File added: {csv_file}")
                file_name = csv_file.name
                if not file_name.endswith(".csv"):
                    logging.warn(f"Invalid file type imported {file_name}")
                    messages.error(
                        request,
                        "Invalid file type selected, please upload right CSV file",
                    )
                    return redirect("..")
                reader = csv.DictReader(csv_file)

                record_created = 0

                for row in reader:
                    logging.debug(f"Row loaded from reader: {row}")
                    name = row["name"]
                    type = row["type"]
                    amount = row["amount"]
                    paid_for = row["paid_for"]
                    paid_by = row["paid_by"]
                    paid_to = row["paid_to"]
                    category = row["category"]
                    group = row["group"]
                    comments = row["comments"]
                    user = row["user"]
                    date = row["date"]
                    createdDate = row["created"]
                    updatedDate = row["updated"]

                    logging.debug(f"Line read for {name}")
                    transaction, created = Transaction.objects.update_or_create(
                        name=name,
                        type=type,
                        amount=amount,
                        paid_for=paid_for,
                        paid_by=paid_by,
                        paid_to=paid_to,
                        category=category,
                        group=group,
                        comments=comments,
                        user=user,
                        date=date,
                        created=createdDate,
                        updated=updatedDate,
                    )

                    if created:
                        record_created = record_created + 1

                    logging.debug(
                        f"Record with transaction {transaction} has been created"
                        if created
                        else f"Record with transaction {transaction} ignored."
                    )
                message = f"Csv file: {file_name} has been imported for {record_created} records."
                logging.info(message)
                self.message_user(request, message)
            return redirect("..")

        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "myfinance/csv_form.html", payload)

    def save_model(self, request, obj, form, change):
        if not change:
            # the object is being created, so set the user
            obj.user = request.user
        obj.save()
