from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from Transaction.models import Transaction
from .serializers import DebtSerializer, TotalDebtSerializer
from decimal import Decimal

# Create your views here.
from Transaction.models import Transaction
from .serializers import TransactionSerializer

class TransactionListAPIView(generics.ListAPIView):
    queryset = Transaction.objects.order_by('-created_at')
    serializer_class = TransactionSerializer


class DebtRelationshipAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.all()
        users = User.objects.all()

        debt_map = {}
        for trans in transactions:
            creditor = trans.creditor.username
            debtor = trans.debtor.username
            amount = Decimal(str(trans.amount))

            if creditor == debtor:
                continue

            key = '->'.join(sorted([creditor, debtor]))

            if key not in debt_map:
                debt_map[key] = {
                    creditor: Decimal('0'),
                    debtor: Decimal('0')
                }

            debt_map[key][creditor] += amount
            debt_map[key][debtor] -= amount

        debts = []
        for key, balances in debt_map.items():
            person1, person2 = key.split('->')
            net_amount = balances[person1]

            if abs(net_amount) > Decimal('0.01'):
                if net_amount > 0:
                    debtor, creditor, amount = person2, person1, net_amount
                else:
                    debtor, creditor, amount = person1, person2, abs(net_amount)
                debts.append({
                    'debtor': debtor,
                    'creditor': creditor,
                    'amount': f"{amount:.2f}"
                })

        return Response(DebtSerializer(debts, many=True).data)

class TotalDebtAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.all()
        user_debt_map = {}

        for user in User.objects.all():
            user_debt_map[user.username] = Decimal('0.00')

        for trans in transactions:
            creditor = trans.creditor.username
            debtor = trans.debtor.username
            amount = Decimal(str(trans.amount))

            if creditor == debtor:
                continue

            user_debt_map[debtor] -= amount
            user_debt_map[creditor] += amount

        # Format the result
        result = []
        for username, net_balance in user_debt_map.items():
            result.append({
                'user': username,
                'net_balance': f"{net_balance:.2f}",  # positive means owed, negative means they owe
            })

        return Response(TotalDebtSerializer(result, many=True).data)