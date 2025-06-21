from itertools import chain
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .forms import *
from .models import *

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Registration successful'})
            
    return redirect('index')


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        authenticateUser = authenticate(request, username=username, password=password)
        
        if authenticateUser is not None:
            login(request, authenticateUser)
            return JsonResponse({'success': True, 'message': 'Login successful'})
        
        return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        
    return redirect('index')



@login_required
def log_out(request):
    logout(request)
    return redirect('index')


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    registration_form = RegistrationForm()
    
    login_form = AuthenticationForm()
    
    context = {
        'registration_form': registration_form,
        'login_form': login_form,
    }
    
    return render(request, 'index.html', context)


@login_required
def dashboard(request):
    
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    income_form = IncomeForm()
    expense_form = ExpenseForm()
    category_form = CategoryForm()
    update_form = UpdateIncomeForm()
    
    income_monthly_data = {}
    expense_monthly_data = {}
    
    for month in months:
        income_monthly_data[month] = 0
        expense_monthly_data[month] = 0

    incomes = Income.objects.filter(user=request.user)
    
    for income in incomes:
        month = income.date.strftime('%B')
        income_monthly_data[month] += income.amount
    
    income_data = [float(y) for y in income_monthly_data.values()]  
    
    
    expenses = Expense.objects.filter(user=request.user)
    
    for expense in expenses:
        month = expense.date.strftime('%B')
        expense_monthly_data[month] += expense.amount
        
    expense_data = [-float(y) if y > 0 else float(y) for y in expense_monthly_data.values()]
    
    
    combined_records = list(chain(incomes, expenses))
    
    sorted_records = sorted(combined_records, key=lambda x: x.created_at)
    
    categories = Category.objects.filter(user=request.user)

    context = {
        'income_form': income_form,
        'expense_form': expense_form,
        'category_form': category_form,
        'income_data': income_data,
        'expense_data': expense_data,
        'total_income': sum(income_data),
        'total_expense': abs(sum(expense_data)),
        'current_balance': sum(sum(income_data), sum(expense_data)),
        'months': months,
        'incomes': incomes,
        'expenses': expenses,
        'update_form': update_form,
        'categories': categories,
        'records': sorted_records
    }

    return render(request, 'dashboard.html', context)



@login_required
def create_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)

        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()

            return JsonResponse({'success': True, 'message': 'Income created successfully'})

    return JsonResponse({'success': False, 'message': 'Invalid form data'})


@login_required
def delete_income(request, income_id):
    if request.method == 'DELETE':
        
        income = Income.objects.filter(user=request.user, id=income_id).last()
        if income:
            income.delete()
            return JsonResponse({'success': True, 'message': 'Income deleted successfully'})
            
    return redirect('dashboard')


@login_required
def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            return JsonResponse({'success': True, 'message': 'Expense created successfully'})

    return JsonResponse({'success': False, 'message': 'Invalid form data'})


@login_required
def delete_expense(request, expense_id):
    if request.method == 'DELETE':

        expense = Expense.objects.filter(user=request.user, id=expense_id).last()
        if expense:
            expense.delete()
            return JsonResponse({'success': True, 'message': 'Expense deleted successfully'})

    return redirect('dashboard')


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()

            return JsonResponse({'success': True, 'message': 'Category created successfully'})

    return JsonResponse({'success': False, 'message': 'Invalid form data'})

@login_required
def delete_category(request, category_id):
    if request.method == 'DELETE':

        category = Category.objects.filter(user=request.user, id=category_id).last()
        if category:
            category.delete()
            return JsonResponse({'success': True, 'message': 'Category deleted successfully'})

    return redirect('dashboard')