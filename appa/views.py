import json
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from .models import Category, Expense, Tag, ExpenseTag
from .forms import CategoryForm, ExpenseForm, TagForm

@method_decorator(csrf_exempt, name='dispatch')
class CategoryList(View):
    def get(self, request):
        data = [{'id': c.id, 'name': c.name, 'description': c.description} for c in Category.objects.all()]
        return JsonResponse({'categories': data})

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        form = CategoryForm(data)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({'id': obj.id, 'name': obj.name, 'description': obj.description}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetail(View):
    def get(self, request, category_id):
        c = get_object_or_404(Category, id=category_id)
        return JsonResponse({'id': c.id, 'name': c.name, 'description': c.description})

    def put(self, request, category_id):
        c = get_object_or_404(Category, id=category_id)
        try:
            data = json.loads(request.body)
            form = CategoryForm(data, instance=c)
            if form.is_valid():
                obj = form.save()
                return JsonResponse({'id': obj.id, 'name': obj.name, 'description': obj.description}, status=200)
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ExpenseList(View):
    def get(self, request):
        data = [{'id': e.id, 'amount': float(e.amount), 'date': e.date.isoformat(), 'description': e.description, 'category_id': e.category_id, 'user_id': e.user_id} for e in Expense.objects.select_related('category', 'user').all()]
        return JsonResponse({'expenses': data})

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        form = ExpenseForm(data)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({'status': 201, 'id': obj.id, 'amount': float(obj.amount), 'date': obj.date.isoformat(), 'category_id': obj.category_id}, status=201)
        return JsonResponse({'status': 400, 'errors': form.errors}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ExpenseDetail(View):
    def get(self, request, expense_id):
        e = get_object_or_404(Expense.objects.select_related('category', 'user'), id=expense_id)
        return JsonResponse({'id': e.id, 'amount': float(e.amount), 'date': e.date.isoformat(), 'description': e.description, 'category_id': e.category_id, 'user_id': e.user_id})

    def put(self, request, expense_id):
        e = get_object_or_404(Expense, id=expense_id)
        try:
            data = json.loads(request.body)
            form = ExpenseForm(data, instance=e)
            if form.is_valid():
                obj = form.save()
                return JsonResponse({'id': obj.id, 'amount': float(obj.amount), 'date': obj.date.isoformat(), 'description': obj.description, 'category_id': obj.category_id, 'user_id': obj.user_id}, status=200)
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

class ExpenseSummaryWeek(View):
    def get(self, request, from_date):
        total = Expense.objects.filter(date__gte=from_date).aggregate(Sum('amount'))['amount__sum'] or 0
        return JsonResponse({'period': 'week', 'from_date': from_date, 'total_amount': float(total)})

class ExpenseSummaryMonth(View):
    def get(self, request, from_date):
        total = Expense.objects.filter(date__gte=from_date).aggregate(Sum('amount'))['amount__sum'] or 0
        return JsonResponse({'period': 'month', 'from_date': from_date, 'total_amount': float(total)})

class ExpenseSummaryYear(View):
    def get(self, request, from_date):
        total = Expense.objects.filter(date__gte=from_date).aggregate(Sum('amount'))['amount__sum'] or 0
        return JsonResponse({'period': 'year', 'from_date': from_date, 'total_amount': float(total)})

@method_decorator(csrf_exempt, name='dispatch')
class TagList(View):
    def get(self, request):
        data = [{'id': t.id, 'name': t.name, 'description': t.description} for t in Tag.objects.all()]
        return JsonResponse({'tags': data})

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        form = TagForm(data)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({'id': obj.id, 'name': obj.name, 'description': obj.description}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class TagDetail(View):
    def get(self, request, tag_id):
        t = get_object_or_404(Tag, id=tag_id)
        return JsonResponse({'id': t.id, 'name': t.name, 'description': t.description})

    def put(self, request, tag_id):
        t = get_object_or_404(Tag, id=tag_id)
        try:
            data = json.loads(request.body)
            form = TagForm(data, instance=t)
            if form.is_valid():
                obj = form.save()
                return JsonResponse({'id': obj.id, 'name': obj.name, 'description': obj.description}, status=200)
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

class ExpenseTags(View):
    def get(self, request, expense_id):
        get_object_or_404(Expense, id=expense_id)
        data = [{'id': et.tag.id, 'name': et.tag.name} for et in ExpenseTag.objects.filter(expense_id=expense_id).select_related('tag')]
        return JsonResponse({'tags': data})

class TagExpensesSummaryWeek(View):
    def get(self, request, tag_id, from_date):
        get_object_or_404(Tag, id=tag_id)
        total = ExpenseTag.objects.filter(tag_id=tag_id, expense__date__gte=from_date).aggregate(Sum('expense__amount'))['expense__amount__sum'] or 0
        return JsonResponse({'tag_id': tag_id, 'period': 'week', 'from_date': from_date, 'total_amount': float(total)})

class TagExpensesSummaryMonth(View):
    def get(self, request, tag_id, from_date):
        get_object_or_404(Tag, id=tag_id)
        total = ExpenseTag.objects.filter(tag_id=tag_id, expense__date__gte=from_date).aggregate(Sum('expense__amount'))['expense__amount__sum'] or 0
        return JsonResponse({'tag_id': tag_id, 'period': 'month', 'from_date': from_date, 'total_amount': float(total)})

class TagExpensesSummaryYear(View):
    def get(self, request, tag_id, from_date):
        get_object_or_404(Tag, id=tag_id)
        total = ExpenseTag.objects.filter(tag_id=tag_id, expense__date__gte=from_date).aggregate(Sum('expense__amount'))['expense__amount__sum'] or 0
        return JsonResponse({'tag_id': tag_id, 'period': 'year', 'from_date': from_date, 'total_amount': float(total)})