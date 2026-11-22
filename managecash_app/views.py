from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from managecash_app.models import *
from managecash_app.forms import *
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm


@login_required
def dashboard_view(req,id):

    if id != req.user.id:
        return redirect('dashboard_view', id=req.user.id)
    
    cash_list = AddCashModel.objects.filter(cash_name_id=id)
    expense_list = ExpenseModel.objects.filter(expense_name_id=id)

    total_cash = 0
    for cash in cash_list:
        total_cash += cash.cash_amount or 0

    total_expense = 0
    for expense in expense_list:
        total_expense += expense.expense_amount or 0

    context={
        'total_cash': total_cash,
        'total_expense': total_expense,
        'balance':total_cash-total_expense,
        'cash_list':cash_list,
        'expense_list':expense_list,
    }
    return render(req,'dashboard.html',context)

def login_view(req):
    form_data=AuthenticationForm()
    if req.method == 'POST':
        form_data=AuthenticationForm(req, data=req.POST)
        if form_data.is_valid():
            user=form_data.get_user()
            if user:
                login(req, user)
                return redirect('dashboard_view', id=user.id)

    context={
            'form_data':form_data,
            'page_title':'login',
            'head_title': 'Login Your Account',
            'btn_title':'Login',
            'extra_link':"register",
            'extra_text':"Don't have any account?",

        }
    return render(req, 'master/base-form.html', context)

def register_view(req):
    form_data=UserForm()
    if req.method == 'POST':
        form_data=UserForm(req.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('login_view')
    context={
            'form_data':form_data,
            'page_title':'register',
            'head_title': 'Register Your Account',
            'btn_title': 'Register',
            'extra_link': "login",
            'extra_text': "Already have an account?",
            }
            
    return render(req, 'master/base-form.html', context)
@login_required
def logout_view(req):
    logout(req)
    return redirect ('login_view')

@login_required
def addcash_view(req):
    form_data=AddCashForm()
    if req.method == 'POST':
        form_data=AddCashForm(req.POST)
        if form_data.is_valid(): 
            data = form_data.save(commit=False)
            data.cash_name = req.user
            data.save()
            return redirect('addcash_list')

    context={
            'form_data':form_data,
            'page_title':'addcash',
            'head_title': 'Add Cash Details',
            'btn_title': 'Add Cash',
            
        }
    return render(req, 'master/base-form.html', context)
@login_required
def addcash_list(req):
    form_data = AddCashModel.objects.filter(cash_name=req.user)
    context={
        'form_data':form_data
    }
    return render(req, 'addcash-list.html', context)
@login_required
def cash_update(req,id):
    data=get_object_or_404(AddCashModel, id=id)
    form_data=AddCashForm(instance=data)
    if req.method == 'POST':
        form_data=AddCashForm(req.POST, instance=data)
        if form_data.is_valid(): 
           data=form_data.save(commit=False)
           data.cash_name=req.user
           data.save()
        return redirect('addcash_list')
    context={
            'form_data':form_data,
            'page_title':'update_addcash',
            'head_title': 'Upadte Cash Details',
            'btn_title': 'Update Cash',
            
        }  
    return render(req, 'master/base-form.html', context) 

def cash_delete(req, id):
    get_object_or_404(AddCashModel, id=id).delete()

    return redirect('addcash_list')
    
@login_required
def add_expense(req):
    form_data=ExpenseForm()
    if req.method == 'POST':
        form_data=ExpenseForm(req.POST)
        if form_data.is_valid(): 
            data = form_data.save(commit=False)
            data.expense_name = req.user
            data.save()
            return redirect('expense_list')
    context={
            'form_data':form_data,
            'page_title':'addexpense',
            'head_title': 'Add Expense Details',
            'btn_title': 'Add Expense',
            
        }  
    return render(req, 'master/base-form.html', context)
@login_required
def expense_list(req):
    form_data=ExpenseModel.objects.filter(expense_name=req.user)
    context={
            'form_data':form_data
        }
    return render(req, 'expense-list.html', context)
@login_required
def update_expense(req, id):
    data=get_object_or_404(ExpenseModel, id=id)
    form_data=ExpenseForm(instance=data)
    if req.method == 'POST':
        form_data=ExpenseForm(req.POST, instance=data)
        if form_data.is_valid(): 
            data = form_data.save(commit=False)
            data.expense_name=req.user
            data.save()
            return redirect('expense_list')
    context={
            'form_data':form_data,
            'page_title':'updateexpense',
            'head_title': 'Update Expense Details',
            'btn_title': 'Update Expense',
            
        }
    return render(req, 'master/base-form.html', context)

def delete_expense(req, id):
    get_object_or_404(ExpenseModel, id=id).delete()
    return redirect('expense_list')