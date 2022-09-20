from __future__ import annotations
from tokenize import group
from django.urls import path

from django.views.generic import TemplateView
from myfinance.views import TransactionView, TransactionDetailView, TransactionCreateView, delete_group, search_transaction, add_category, delete_category, transactions, transaction_view, category, group, delete_group, add_group

app_name = "myfinance"
urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("transactions/", transactions, name="transactions"),
    path("categories/", category, name="categories"),
    path("groups/", group, name="groups"),
    path(r'^/(?P<pk>[0-9]+)/$', TransactionDetailView.as_view(), name="transaction-detail"),
    path("create_transaction/", TransactionCreateView.as_view(), name="create-transaction"),
    path("search_transaction/", search_transaction, name="search-transaction"),
    path('add_category/', add_category, name='add-category'),
    path('add_group/', add_group, name='add-group'),
    path('delete_category/<int:pk>/', delete_category, name='delete-category'),
    path('delete_group/<int:pk>/', delete_group, name='delete-group')
]
