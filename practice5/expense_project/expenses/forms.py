from django.forms import ModelForm, CheckboxSelectMultiple, ModelMultipleChoiceField
from .models import Expense, Category, GroupExpense
from django.contrib.auth.models import User

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)  # Filter categories by user


class GroupExpenseForm(ModelForm):
    users = ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=CheckboxSelectMultiple
    )

    class Meta:
        model = GroupExpense
        fields = ['name', 'amount', 'date', 'users']