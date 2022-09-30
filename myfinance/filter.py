import django_filters

from .models import Transaction, Category, Group
from .forms import TransactionFilterForm

class TransactionFilter(django_filters.FilterSet):

    # category = django_filters.ModelChoiceFilter(queryset=Category)
    # category = django_filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    # group = django_filters.CharFilter(field_name='group__name', lookup_expr='iexact')
    name = django_filters.CharFilter(lookup_expr='icontains')
    comments = django_filters.CharFilter(lookup_expr='icontains')
    # date_year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    # date_year__gt = django_filters.NumberFilter(field_name='date', lookup_expr='year__gt')
    # date_year__lt = django_filters.NumberFilter(field_name='date', lookup_expr='year__lt')

    class Meta:
        model = Transaction
        form = TransactionFilterForm
        # fields = {
        #     'group__name': ['iexact'],
        # }
        fields = ['group', 'category']