import imp
from sre_parse import CATEGORIES
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView
from myfinance.models import Transaction, Category
from myfinance.forms import CategoryForm
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.db.models import Q
from django.contrib.auth.decorators import login_required

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
    page_num = request.GET.get("page", "1")
    page = Paginator(object_list=Transaction.objects.all(), per_page=10).get_page(page_num)

    if request.htmx:
        base_template = "myfinance_partial.html"
        template = "myfinance/transaction/transaction_list.html"
    else:
        base_template = "myfinance_base.html"
        template = "myfinance/transaction/transaction_home.html"

    return render(request, template, {
        # "base_template": base_template, 
        "page": page})


@require_GET
@login_required
def search_transaction(request: HtmxHttpRequest) -> HttpResponse:
    name = request.GET.get("name")
    page_num = request.GET.get("page", "1")
    queryset = Transaction.objects.filter(Q(name__icontains=name) | Q(comments__icontains=name))
    page = Paginator(object_list=queryset, per_page=10).get_page(page_num)

    if request.htmx:
        base_template = "myfinance_partial.html"
        template = "myfinance/transaction/transaction_list.html"
    else:
        base_template = "myfinance_base.html"
        template = "myfinance/transaction/transaction_home.html"

    return render(request, template, {
        # "base_template": base_template, 
        "page": page})


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
def delete_category(request, pk):
    # remove the contact from list.
    category_id = Category.objects.get(id=pk)
    category_id.delete()

    message = f'Category with id {pk} deleted'
    return redirect('myfinance:categories')


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
