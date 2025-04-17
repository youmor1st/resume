from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from . import views
from .views import add_category, add_group_expense, group_expense_list

def redirect_to_login(request):
    return redirect('/accounts/')

urlpatterns = [
    path('', redirect_to_login),
    path('accounts/', include('allauth.urls')),
    path('expenses/', login_required(views.index), name='index'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('categories/add/', add_category, name='add_category'),
    path('group_expenses/add/', add_group_expense, name='add_group_expense'),
    path('group_expenses/', group_expense_list, name='group_expense_list'),
]