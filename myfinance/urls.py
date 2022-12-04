from __future__ import annotations
from tokenize import group
from django.urls import path

from django.views.generic import TemplateView
from myfinance.views import TransactionView, TransactionDetailView, TransactionCreateView, add_transaction, delete_group, delete_transaction, search_transaction, add_category, delete_category, transactions, transaction_view, category, group, delete_group, add_group, delete_transaction

app_name = "myfinance"
urlpatterns = [

    # Home
    path("", TemplateView.as_view(template_name="myfinance/myfinance_home.html"), name="home"),

    path("transactions/", transactions, name="transactions"),
    path("categories/", category, name="categories"),
    path("groups/", group, name="groups"),
    path('transaction-detail/<int:pk>', TransactionDetailView.as_view(), name="transaction-detail"),
    path("create_transaction/", TransactionCreateView.as_view(), name="create-transaction"),

    # Search
    path("search_transaction/", search_transaction, name="search-transaction"),

    # Add
    path('add_transaction/', add_transaction, name='add-transaction'),
    path('add_category/', add_category, name='add-category'),
    path('add_group/', add_group, name='add-group'),

    # Delete
    path('delete_transaction/<int:pk>/', delete_transaction, name='delete-transaction'),
    path('delete_category/<int:pk>/', delete_category, name='delete-category'),
    path('delete_group/<int:pk>/', delete_group, name='delete-group')
]
