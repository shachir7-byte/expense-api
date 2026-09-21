from django import forms
from .models import Category, Expense, Tag

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description', 'user']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'description']