import imp
from re import search, template
from sre_parse import CATEGORIES
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView
from myfinance.models import Transaction, Category, Group
from myfinance.forms import CategoryForm, GroupForm, TransactionForm
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchRank

from .filter import TransactionFilter

from django_htmx.middleware import HtmxDetails
from django.core.paginator import Paginator

# Create your views here.
# Typing pattern recommended by django-stubs:
# https://github.com/typeddjango/django-stubs#how-can-i-create-a-httprequest-thats-guaranteed-to-have-an-authenticated-user
class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


class TransactionView(ListView):
    model = Transaction


class TransactionDetailView(DetailView):
    model = Transaction


class TransactionCreateView(CreateView):
    model = Transaction
    fields = ["name", "type", "amount", "paid_for", "paid_by", "paid_to", "category", "group", "date", "comments"]


@require_GET
@login_required
def category(request: HtmxHttpRequest) -> HttpResponse:
    page_num = request.GET.get("page", "1")
    page = Paginator(object_list=Category.objects.all(), per_page=10).get_page(page_num)

    if request.htmx:
        base_template = "myfinance_partial.html"
        template = "myfinance/category/category_list.html"
    else:
        base_template = "myfinance_base.html"
        template = "myfinance/category/category_home.html"

    return render(request, template, {
        # "base_template": base_template, 
        "page": page})

@require_POST
@login_required
def add_category(request: HtmxHttpRequest) -> HttpResponse:
    form = CategoryForm(request.POST)
    if form.is_valid():
        name = form.save()
        page_num = request.GET.get("page", "1")
        page = Paginator(object_list=Category.objects.all(), per_page=10).get_page(page_num)
    return render(
        request,
        "myfinance/category/category_list.html",
        {"form": form, "page": page},
    )


# @require_http_methods(["GET", "POST"])
# def category(request):

#     template_name = 'category_list.html'
#     form = CategoryForm(request.POST)
#     page_num = request.GET.get("page", "1")
#     page = Paginator(object_list=Category.objects.all(), per_page=10).get_page(page_num)

#     if request.method == 'POST':
#         print('POST request')
#         if form.is_valid():
#             name = form.save()
#             message = f'Category {name} added succesfully'
#             page_num = request.GET.get("page", "1")
#             page = Paginator(object_list=Category.objects.all(), per_page=10).get_page(page_num)
#             return render(request, 'myfinance/category/category_home.html', {'page': page, 'form': form, 'message': message})

#     else:
#         print('GET request')
#         return render(request, 'myfinance/category/category_home.html', {'page': page, 'form': form})



    name = request.POST.get('name')
    comments = request.POST.get('comments')

    category = Category.objects.create(name=name, comments=comments)
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


@require_GET
@login_required
def transactions(request: HtmxHttpRequest) -> HttpResponse:

    transactions = TransactionFilter(request.GET, queryset=Transaction.objects.all())
    page_num = request.GET.get("page", "1")
    page = Paginator(object_list=transactions.qs, per_page=10).get_page(page_num)
    # total_amount = Transaction.objects.aggregate(Sum('amount'))['amount__sum']
    # total_transactions = Transaction.objects.count()

    # if request.htmx:
    #     base_template = "myfinance_partial.html"
    #     template = "myfinance/transaction/transaction_list.html"
    # else:
    #     base_template = "myfinance_base.html"
    #     template = "myfinance/transaction/transaction_home.html"

    # return render(request, template, {
    #     # "base_template": base_template, 
    #     "page": page, "total": total_amount, "total_transactions": total_transactions})

    

    # queryset = Transaction.objects.annotate(search=SearchVector('name', 'comments', 'paid_to')).filter(search=name)
    #  (Q(name__icontains=name) | Q(comments__icontains=name) | Q(paid_to__icontains=name))
    # page = Paginator(object_list=transactions.qs, per_page=10).get_page(page_num)

    total_amount = transactions.qs.aggregate(Sum('amount'))['amount__sum']
    total_transactions = transactions.qs.count()

    print(f'Total: {total_amount}, transactions: {total_transactions}')

    if request.htmx:
        print("HTMX request")
        base_template = "myfinance_partial.html"
        template = "myfinance/transaction/transaction_list.html"
    else:
        print("Normal request")
        base_template = "myfinance_base.html"
        template = "myfinance/transaction/transaction_home.html"

    # template = "myfinance/transaction_list.html"

    return render(request, template, {
        "base_template": base_template, 
         "total": total_amount, "total_transactions": total_transactions, "page": page, "transactions": transactions})


@require_GET
@login_required
def search_transaction(request: HtmxHttpRequest) -> HttpResponse:
    name = request.GET.get("name")
    after = request.GET.get("after")
    before = request.GET.get("before")
    frequency = request.GET.get("frequency")
    page_num = request.GET.get("page", "1")

    if name:
        print(name)
    if after:
        print(after)
    if before:
        print(before)
    if frequency:
        print(frequency)

    transactions = TransactionFilter(request.GET, queryset=Transaction.objects.all())

    # queryset = Transaction.objects.annotate(search=SearchVector('name', 'comments', 'paid_to')).filter(search=name)
    #  (Q(name__icontains=name) | Q(comments__icontains=name) | Q(paid_to__icontains=name))
    page = Paginator(object_list=transactions.qs, per_page=10).get_page(page_num)

    total_amount = transactions.qs.aggregate(Sum('amount'))['amount__sum']
    total_transactions = transactions.qs.count()

    print(f'Total: {total_amount}, transactions: {total_transactions}')

    if request.htmx:
        base_template = "myfinance_partial.html"
        template = "myfinance/transaction/transaction_list.html"
    else:
        base_template = "myfinance_base.html"
        template = "myfinance/transaction/transaction_home.html"

    template = "myfinance/transaction_list.html"

    return render(request, template, {
        # "base_template": base_template, 
        "page": page, "total": total_amount, "total_transactions": total_transactions, "transactions": transactions})


@require_http_methods(["GET", "POST"])
@login_required
def add_transaction(request: HtmxHttpRequest) -> HttpResponse:
    form = TransactionForm(request.POST)
    template = "myfinance/transaction/transaction_add.html"

    if request.method == 'GET':
        print('Get Request')

    else:

        print('Adding Transaction')

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

        return  redirect('myfinance:transactions')
    return render(request, template, {"form": form})


@require_GET
@login_required
def group(request: HtmxHttpRequest) -> HttpResponse:

    print('Getting groups')

    page_num = request.GET.get("page", "1")
    page = Paginator(object_list=Group.objects.all(), per_page=10).get_page(page_num)

    if request.htmx:
        base_template = "myfinance_partial.html"
        template = "myfinance/group/group_list.html"
    else:
        base_template = "myfinance_base.html"
        template = "myfinance/group/group_home.html"

    return render(request, template, {
        # "base_template": base_template, 
        "page": page})


@require_POST
@login_required
def add_group(request: HtmxHttpRequest) -> HttpResponse:
    form = GroupForm(request.POST)

    print('Adding group')

    if form.is_valid():
        name = form.save()
        page_num = request.GET.get("page", "1")
        page = Paginator(object_list=Group.objects.all(), per_page=10).get_page(page_num)
    return render(
        request,
        "myfinance/group/group_list.html",
        {"form": form, "page": page},
    )


@require_GET
@login_required
def category_view(request: HtmxHttpRequest) -> HttpResponse:
    # Standard Django pagination
    page_num = request.GET.get("page", "1")
    print(page_num)
    page = Paginator(object_list=Category.objects.all(), per_page=10).get_page(page_num)

    # The htmx magic - use a different, minimal base template for htmx
    # requests, allowing us to skip rendering the unchanging parts of the
    # template.

    if request.htmx:
        base_template = "myfinance_base.html"
    else:
        base_template = "myfinance_base.html"

    return render(
        request,
        "myfinance/category.html",
        {
            "base_template": base_template,
            "page": page,
        },
    )


@login_required
def delete_transaction(request, pk):
    # remove the contact from list.
    transaction_id = Transaction.objects.get(id=pk)
    transaction_id.delete()

    message = f'Transaction with id {pk} deleted'
    return redirect('myfinance:transactions')


@login_required
def delete_category(request, pk):
    # remove the contact from list.
    category_id = Category.objects.get(id=pk)
    category_id.delete()

    message = f'Category with id {pk} deleted'
    return redirect('myfinance:categories')


@login_required
def delete_group(request, pk):
    # remove the contact from list.
    group_id = Group.objects.get(id=pk)
    group_id.delete()

    message = f'Group with id {pk} deleted'
    return redirect('myfinance:groups')


@require_GET
@login_required
def transaction_view(request: HtmxHttpRequest) -> HttpResponse:
    # Standard Django pagination
    page_num = request.GET.get("page", "1")
    print(page_num)
    page = Paginator(object_list=Transaction.objects.all(), per_page=10).get_page(page_num)

    # The htmx magic - use a different, minimal base template for htmx
    # requests, allowing us to skip rendering the unchanging parts of the
    # template.

    if request.htmx:
        base_template = "myfinance_partial.html"
    else:
        base_template = "myfinance_base.html"

    return render(
        request,
        "myfinance/transactions.html",
        {
            "base_template": base_template,
            "page": page,
        },
    )
