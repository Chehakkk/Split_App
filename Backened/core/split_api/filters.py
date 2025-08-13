# filters.py
import django_filters
from .models import Expense

class ExpenseFilter(django_filters.FilterSet):
    group = django_filters.UUIDFilter(field_name='group__id')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    created_at__gte = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Expense
        fields = ['group', 'category', 'created_at__gte', 'created_at__lte']