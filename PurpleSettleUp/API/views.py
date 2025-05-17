from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Q
from Transaction.models import Transaction, PaymentVerification
from User.models import Notification
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
        # Get all transactions
        transactions = Transaction.objects.all()
        
        # Get all pending verifications
        pending_verifications = PaymentVerification.objects.filter(
            Q(payer=request.user) | Q(receiver=request.user),
            status='pending'
        )

        # Get notifications for pending verifications where the current user is the receiver
        notifications = Notification.objects.filter(
            recipient=request.user,
            notification_type='payment',
            verification_id__in=pending_verifications.filter(receiver=request.user).values_list('id', flat=True)
        ).values('id', 'verification_id')

        # Create a mapping of verification_id to notification_id
        notification_map = {n['verification_id']: n['id'] for n in notifications}
        print("Notification map:", notification_map)  # Debug log

        debt_map = {}
        
        # First, process all transactions
        for trans in transactions:
            creditor = trans.creditor.username
            debtor = trans.debtor.username
            amount = Decimal(str(trans.amount))

            if creditor == debtor:
                continue

            key = '->'.join(sorted([creditor, debtor]))

            if key not in debt_map:
                debt_map[key] = {
                    creditor: {'amount': Decimal('0'), 'verification_id': None, 'notification_id': None, 'status': 'active'},
                    debtor: {'amount': Decimal('0'), 'verification_id': None, 'notification_id': None, 'status': 'active'}
                }

            debt_map[key][creditor]['amount'] += amount
            debt_map[key][debtor]['amount'] -= amount

        # Then, process pending verifications
        for verification in pending_verifications:
            payer = verification.payer.username
            receiver = verification.receiver.username
            amount = verification.amount

            key = '->'.join(sorted([payer, receiver]))

            if key not in debt_map:
                debt_map[key] = {
                    payer: {'amount': Decimal('0'), 'verification_id': None, 'notification_id': None, 'status': 'active'},
                    receiver: {'amount': Decimal('0'), 'verification_id': None, 'notification_id': None, 'status': 'active'}
                }

            # Mark both sides as pending
            debt_map[key][payer]['verification_id'] = verification.id
            debt_map[key][receiver]['verification_id'] = verification.id
            # Only set notification_id for the receiver (who needs to verify)
            if verification.id in notification_map:
                debt_map[key][receiver]['notification_id'] = notification_map[verification.id]
                print(f"Setting notification_id {notification_map[verification.id]} for receiver {receiver}")  # Debug log
            debt_map[key][payer]['status'] = 'pending'
            debt_map[key][receiver]['status'] = 'pending'

        debts = []
        for key, balances in debt_map.items():
            person1, person2 = key.split('->')
            net_amount = balances[person1]['amount']

            if abs(net_amount) > Decimal('0.01') or balances[person1]['status'] == 'pending':
                if net_amount > 0:
                    debtor, creditor = person2, person1
                    amount = net_amount
                    verification_id = balances[person2]['verification_id']
                    notification_id = balances[person2]['notification_id']
                    status = balances[person2]['status']
                else:
                    debtor, creditor = person1, person2
                    amount = abs(net_amount)
                    verification_id = balances[person1]['verification_id']
                    notification_id = balances[person1]['notification_id']
                    status = balances[person1]['status']

                debt = {
                    'debtor': debtor,
                    'creditor': creditor,
                    'amount': f"{amount:.2f}",
                    'verification_id': verification_id,
                    'notification_id': notification_id,
                    'status': status
                }
                print("Adding debt:", debt)  # Debug log
                debts.append(debt)

        return Response(debts)

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

            # Only count non-pending transactions in the total
            if not PaymentVerification.objects.filter(
                transaction=trans,
                status='pending'
            ).exists():
                user_debt_map[debtor] -= amount
                user_debt_map[creditor] += amount

        # Format the result
        result = []
        for username, net_balance in user_debt_map.items():
            result.append({
                'user': username,
                'net_balance': f"{net_balance:.2f}",  # positive means owed, negative means they owe
            })

        return Response(result)