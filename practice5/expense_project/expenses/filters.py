import django_filters
from .models import Expense


class ExpenseFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()
    category = django_filters.ModelChoiceFilter(queryset=Expense.objects.none())

    class Meta:
        model = Expense
        fields = ['date', 'category']

    def __init__(self, *args, **kwargs):
        user = kwargs['queryset'].model.objects.first().user if kwargs['queryset'].exists() else None
        super().__init__(*args, **kwargs)
        if user:
            self.filters['category'].queryset = user.category_set.all()
