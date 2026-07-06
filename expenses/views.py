from datetime import date

from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import request, status
from drf_yasg.utils import swagger_auto_schema
from .models import Expense
from .serializers import ExpenseSerializer
from drf_yasg import openapi

@swagger_auto_schema(
    method="get",
    operation_summary="Get all expenses",
    operation_description="""
Returns all expenses belonging to the authenticated user.

Features:
- Pagination (5 records per page)
- Search by title
- Filter by category
""",
    responses={
        200: ExpenseSerializer(many=True),
        401: "Unauthorized",
    },
)

@swagger_auto_schema(
    method="post",
    operation_summary="Create expense",
    operation_description="Create a new expense for the authenticated user.",
    request_body=ExpenseSerializer,
    responses={
        201: ExpenseSerializer,
        400: "Validation Error",
        401: "Unauthorized",
    },
)
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

@swagger_auto_schema(
    method="get",
    operation_summary="Expense summary",
    operation_description="Returns total expenses grouped into major categories."
)

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

@swagger_auto_schema(
    method="get",
    operation_summary="Monthly summary",
    operation_description="Returns expense statistics for the current month."
)

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

@swagger_auto_schema(
    method="get",
    operation_summary="Category summary",
    operation_description="Returns total expenses grouped by category."
)

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

@swagger_auto_schema(
    method="get",
    operation_summary="Get expense by ID",
    operation_description="Returns one expense belonging to the logged-in user.",
    responses={
        200: ExpenseSerializer,
        404: "Expense not found",
    },
)

@swagger_auto_schema(
    method="put",
    operation_summary="Update expense",
    operation_description="Update an existing expense.",
    request_body=ExpenseSerializer,
    responses={
        200: ExpenseSerializer,
        400: "Validation Error",
        404: "Expense not found",
    },
)

@swagger_auto_schema(
    method="delete",
    operation_summary="Delete expense",
    operation_description="Delete an expense.",
    responses={
        204: "Expense deleted successfully",
        404: "Expense not found",
    },
)

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

@swagger_auto_schema(
    method="get",
    operation_summary="Dashboard",
    operation_description="Returns dashboard statistics including total expense, monthly expense, and category-wise totals."
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

    permission_classes = [IsAuthenticated]

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
    
    @swagger_auto_schema(
        request_body=ExpenseSerializer,
        responses={201: ExpenseSerializer},
    )
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
        return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


class ExpenseDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            expense = Expense.objects.get(pk=pk, user=request.user)
        except Expense.DoesNotExist:
            return Response(
            {"error": "Expense not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ExpenseSerializer,
        responses={200: ExpenseSerializer},
    )
    def put(self, request, pk):
        return Response({"message": "PUT working"})

    def delete(self, request, pk):
        return Response({"message": "DELETE working"})