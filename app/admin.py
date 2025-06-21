from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    search_fields = ('name', 'type')
    
@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'source', 'date', 'category', 'description', 'created_at', 'updated_at')
    search_fields = ('amount', 'category', 'user')
    
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category', 'date', 'description', 'receipt_image', 'created_at', 'updated_at')
    search_fields = ('amount', 'category', 'user', 'description', 'date')
