from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer
from datetime import date
from django.db.models import Sum
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from drf_yasg.utils import swagger_auto_schema


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def expense_list(request):

    if request.method == "GET":
        category = request.GET.get("category")
        search = request.GET.get("search")
        expenses = Expense.objects.filter(user=request.user).order_by("-created_at")
        if category:
            expenses = expenses.filter(category=category)
        if search:
            expenses = expenses.filter(title__icontains=search)

        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(expenses, request)
        serializer = ExpenseSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == "POST":
        serializer = ExpenseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)

        return Response(serializer.errors)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def expense_summary(request):
    expenses = Expense.objects.filter(user=request.user)
    total = expenses.aggregate(Sum("amount"))["amount__sum"] or 0
    food = expenses.filter(category="Food").aggregate(Sum("amount"))["amount__sum"] or 0
    travel = expenses.filter(category="Travel").aggregate(Sum("amount"))["amount__sum"] or 0
    shopping = expenses.filter(category="Shopping").aggregate(Sum("amount"))["amount__sum"] or 0

    return Response({
        "total_expense": total,
        "food": food,
        "travel": travel,
        "shopping": shopping,
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def monthly_summary(request):

    today = date.today()

    expenses = Expense.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month
    )

    total = expenses.aggregate(Sum("amount"))["amount__sum"] or 0

    count = expenses.count()

    return Response({
        "month": today.strftime("%B"),
        "year": today.year,
        "total_expense": total,
        "number_of_expenses": count
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def category_summary(request):

    expenses = Expense.objects.filter(user=request.user)

    data = expenses.values("category").annotate(
        total=Sum("amount")
    ).order_by("-total")

    return Response(data)

@swagger_auto_schema(
    method="put",
    request_body=ExpenseSerializer,
    responses={200: ExpenseSerializer},
)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def expense_detail(request, pk):

    try:
        expense = Expense.objects.get(pk=pk, user=request.user)
    except Expense.DoesNotExist:
        return Response({"error": "Expense not found"})

    if request.method == "GET":
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ExpenseSerializer(expense, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == "DELETE":
        expense.delete()
        return Response({"message": "Expense deleted successfully"})
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):

    expenses = Expense.objects.filter(user=request.user)

    total_expense = expenses.aggregate(total=Sum("amount"))["total"] or 0

    today = date.today()

    monthly_expense = expenses.filter(
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum("amount"))["total"] or 0

    category_data = expenses.values("category").annotate(
        total=Sum("amount")
    ).order_by("-total")

    return Response({
        "total_expense": total_expense,
        "monthly_expense": monthly_expense,
        "category_summary": category_data
    })