from django.urls import path
from .views import TransactionListAPIView, DebtRelationshipAPIView, TotalDebtAPIView


urlpatterns = [
    path('transactions/', TransactionListAPIView.as_view(), name='transactions'),
    path('debts/', DebtRelationshipAPIView.as_view(), name='debts'),
    path('debts/total/', TotalDebtAPIView.as_view(), name='total-debt'),  # New endpoint
]
