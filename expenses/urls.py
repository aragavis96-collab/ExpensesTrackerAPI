from django.urls import path
from . import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Expense Tracker API",
        default_version="v1",
        description="Expense Tracker REST API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", views.ExpenseListCreateView.as_view(), name="expense-list"),
    path("<int:pk>/", views.ExpenseDetailView.as_view(), name="expense-detail"),
    path("summary/", views.expense_summary),
    path("monthly-summary/", views.monthly_summary),
    path("category-summary/", views.category_summary),
    path("dashboard/", views.dashboard),

    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]