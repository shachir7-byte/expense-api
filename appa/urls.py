from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryList.as_view()),
    path('categories/<int:category_id>/', views.CategoryDetail.as_view()),
    path('expenses/', views.ExpenseList.as_view()),
    path('expenses/<int:expense_id>/', views.ExpenseDetail.as_view()),
    path('expenses/summary/', views.ExpenseSummary.as_view()),
    path('tags/', views.TagList.as_view()),
    path('tags/<int:tag_id>/', views.TagDetail.as_view()),
    path('expenses/<int:expense_id>/tags/', views.ExpenseTags.as_view()),
    path('tags/<int:tag_id>/expenses/summary/', views.TagExpensesSummary.as_view()),
]