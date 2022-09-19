from __future__ import annotations
from django.urls import path

from django.views.generic import TemplateView
from myfinance.views import TransactionView, TransactionDetailView, TransactionCreateView, search_transaction, add_category, delete_category, transactions, transaction_view, category

app_name = "myfinance"
urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("transactions/", transactions, name="transactions"),
    path("categories/", category, name="categories"),
    path(r'^/(?P<pk>[0-9]+)/$', TransactionDetailView.as_view(), name="transaction-detail"),
    path("create_transaction/", TransactionCreateView.as_view(), name="create-transaction"),
    path("search_transaction/", search_transaction, name="search-transaction"),
    path('add_category/', add_category, name='add-category'),
    path('delete_category/<int:pk>/', delete_category, name='delete-category')
]
