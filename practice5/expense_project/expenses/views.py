from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm, CategoryForm, GroupExpenseForm
from .models import Expense, Category, GroupExpense
from django.db.models import Sum
from datetime import datetime, timedelta
from .filters import ExpenseFilter


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('add_category')
    else:
        form = CategoryForm()

    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'expenses/add_category.html', {'form': form, 'categories': categories})


@login_required
def index(request):
    if request.method == "POST":
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense = expense_form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('index')

    expenses = Expense.objects.filter(user=request.user)
    expense_filter = ExpenseFilter(request.GET, queryset=expenses)
    expenses = expense_filter.qs
    total_expenses = expenses.aggregate(Sum('amount'))

    last_year = datetime.today() - timedelta(days=365)
    data = Expense.objects.filter(date__gt=last_year)
    yearly_sum = data.aggregate(Sum('amount'))

    last_month = datetime.today() - timedelta(days=30)
    data = Expense.objects.filter(date__gt=last_month)
    monthly_sum = data.aggregate(Sum('amount'))

    last_week = datetime.today() - timedelta(days=7)
    data = Expense.objects.filter(date__gt=last_week)
    weekly_sum = data.aggregate(Sum('amount'))

    daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))
    categorical_sums = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))

    expense_form = ExpenseForm()
    return render(request, 'expenses/index.html', {'expense_form': expense_form,
                                                'expenses': expenses, 'filter': expense_filter,
                                                'total_expenses': total_expenses, 'yearly_sum': yearly_sum,
                                                'monthly_sum': monthly_sum, 'weekly_sum': weekly_sum,
                                                'daily_sums': daily_sums,
                                                'categorical_sums': categorical_sums})


@login_required
def edit(request, id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)

    if request.method == "POST":
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid:
            form.save()
            return redirect('index')
    return render(request, 'expenses/edit.html', {'expense_form': expense_form})


@login_required
def delete(request, id):
    if request.method == "POST" and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')


@login_required
def add_group_expense(request):
    if request.method == 'POST':
        form = GroupExpenseForm(request.POST)
        if form.is_valid():
            group_expense = form.save()
            return redirect('group_expense_list')  # Redirect to expense list
    else:
        form = GroupExpenseForm()

    return render(request, 'expenses/group_expense_form.html', {'form': form})


@login_required
def group_expense_list(request):
    expenses = GroupExpense.objects.all()
    return render(request, 'expenses/group_expense_list.html', {'expenses': expenses})