from datetime import date

from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from .models import Expense
from .serializers import ExpenseSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def expense_list(request):

    if request.method == "GET":
        category = request.GET.get("category")
        search = request.GET.get("search")

        expenses = Expense.objects.filter(
            user=request.user
        ).order_by("-created_at")

        if category:
            expenses = expenses.filter(category=category)

        if search:
            expenses = expenses.filter(title__icontains=search)

        paginator = PageNumberPagination()
        paginator.page_size = 5

        result_page = paginator.paginate_queryset(expenses, request)
        serializer = ExpenseSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    serializer = ExpenseSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def expense_summary(request):

    expenses = Expense.objects.filter(user=request.user)

    return Response({
        "total_expense": expenses.aggregate(Sum("amount"))["amount__sum"] or 0,
        "food": expenses.filter(category="Food").aggregate(Sum("amount"))["amount__sum"] or 0,
        "travel": expenses.filter(category="Travel").aggregate(Sum("amount"))["amount__sum"] or 0,
        "shopping": expenses.filter(category="Shopping").aggregate(Sum("amount"))["amount__sum"] or 0,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def monthly_summary(request):

    today = date.today()

    expenses = Expense.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month,
    )

    return Response({
        "month": today.strftime("%B"),
        "year": today.year,
        "total_expense": expenses.aggregate(Sum("amount"))["amount__sum"] or 0,
        "number_of_expenses": expenses.count(),
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def category_summary(request):

    expenses = Expense.objects.filter(user=request.user)

    data = (
        expenses.values("category")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    return Response(data)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def expense_detail(request, pk):

    try:
        expense = Expense.objects.get(pk=pk, user=request.user)
    except Expense.DoesNotExist:
        return Response(
            {"error": "Expense not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = ExpenseSerializer(expense, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    expense.delete()

    return Response(
        {"message": "Expense deleted successfully"},
        status=status.HTTP_204_NO_CONTENT,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):

    expenses = Expense.objects.filter(user=request.user)

    today = date.today()

    category_data = (
        expenses.values("category")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    return Response({
        "total_expense": expenses.aggregate(total=Sum("amount"))["total"] or 0,
        "monthly_expense": expenses.filter(
            date__year=today.year,
            date__month=today.month,
        ).aggregate(total=Sum("amount"))["total"] or 0,
        "category_summary": category_data,
    })

class ExpenseListCreateView(APIView):
    
    def get(self, request):
        category = request.GET.get("category")
        search = request.GET.get("search")

        expenses = Expense.objects.filter(
            user=request.user
        ).order_by("-created_at")

        if category:
            expenses = expenses.filter(category=category)

        if search:
            expenses = expenses.filter(title__icontains=search)

        paginator = PageNumberPagination()
        paginator.page_size = 5

        result_page = paginator.paginate_queryset(expenses, request)
        serializer = ExpenseSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)