from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from string import digits

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'source', 'date', 'category', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date', 'description', 'receipt_image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        

class UpdateIncomeForm(forms.ModelForm):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'step': '0.01'}), required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category', required=True)
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'rows': 3}), required=True)