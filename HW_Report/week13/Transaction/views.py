from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Transaction, SharedExpense, ExpenseShare, PaymentVerification
from User.models import Notification
from decimal import Decimal
import requests
import json
from django.conf import settings
from API.views import DebtRelationshipAPIView, TotalDebtAPIView
from rest_framework.test import APIRequestFactory
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from User.utils import create_notification
from django.db import transaction as db_transaction
from django.utils import timezone
import uuid
import hmac
import base64
import hashlib
import time

# Create your views here.
@login_required
def history(request):
    transactions = []
    users = []
    debts = []
    context = {
        'transactions': transactions,
        'users': users,
        'debts': debts
    }
    return render(request, 'history.html', context)

@login_required
def single_transaction(request, slug):
    try:
        transaction = Transaction.objects.get(slug=slug)
        context = {
            'transaction': transaction
        }
        return render(request, 'single_transaction.html', context)
    except Transaction.DoesNotExist:
        messages.error(request, 'Transaction not found.')
        return redirect('history')

@login_required
def add_transaction(request):
    if request.method == 'POST':
        paid_by_id = request.POST.get('paid_by')
        amount = Decimal(request.POST.get('amount'))
        description = request.POST.get('description', '')
        shared_with_ids = request.POST.getlist('shared_with')

        try:
            with db_transaction.atomic():
                # Get the user who paid
                paid_by = User.objects.get(id=paid_by_id)
                
                # Create the shared expense
                shared_expense = SharedExpense.objects.create(
                    paid_by=paid_by,
                    amount=amount,
                    description=description
                )

                # Calculate share amount (divide equally among all participants including the payer)
                total_participants = len(shared_with_ids)  # No need to add 1 since payer is included in shared_with
                if total_participants == 0:
                    raise ValueError("Please select at least one person to share the expense with")
                
                share_amount = amount / Decimal(total_participants)
                print("Share amount:", share_amount)

                # Create expense shares for all participants
                for user_id in shared_with_ids:
                    user = User.objects.get(id=user_id)
                    
                    # Create the expense share record
                    ExpenseShare.objects.create(
                        expense=shared_expense,
                        user=user,
                        share_amount=share_amount
                    )
                    print("Expense share created for user:", user.username)

                    # Create a transaction record for each participant except the payer
                    if user != paid_by:
                        Transaction.objects.create(
                            creditor=paid_by,
                            debtor=user,
                            amount=share_amount,
                            description=description,
                            shared_expense=shared_expense
                        ).save()
                        # Create notification for the debtor
                        create_notification(
                            user=user,
                            notification_type='debt',
                            title='New Shared Expense Added',
                            message=f'{paid_by.username} added a shared expense of ${amount} ({description}). Your share is ${share_amount}.',
                            send_email=True
                        )

                messages.success(request, 'Expense added and split successfully!')
                return redirect('/transaction/history')

        except User.DoesNotExist:
            messages.error(request, 'One or more selected users do not exist.')
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    # Get all users for the template
    all_users = User.objects.all()
    return render(request, 'add_transaction.html', {'all_users': all_users})

@login_required
def my_debt(request):
    try:
        # Get all transactions where the current user is either the creditor or debtor
        user_transactions = Transaction.objects.filter(
            Q(creditor=request.user) | Q(debtor=request.user)
        ).exclude(
            amount=None  # Exclude transactions with no amount
        ).order_by('-created_at')

        # Create API factory
        factory = APIRequestFactory()
        api_request = factory.get('/')
        api_request.user = request.user

        # Get debt relationships
        debt_view = DebtRelationshipAPIView()
        debt_response = debt_view.get(api_request)
        debt_relationships = debt_response.data

        # Get total balance
        total_view = TotalDebtAPIView()
        total_response = total_view.get(api_request)
        total_balance = total_response.data
        print(debt_relationships)
        # Convert amount fields to numerical values
        for debt in debt_relationships:
            debt['amount'] = float(debt['amount'])

        context = {
            'transactions': user_transactions,
            'debts': debt_relationships,
            'total_balance': total_balance
        }

        return render(request, 'my_debt.html', context)
    except Exception as e:
        messages.error(request, f'An error occurred: {e}')
        return redirect('/')

@require_http_methods(["POST"])
@csrf_protect
@login_required
def cancel_debt(request):
    try:
        data = json.loads(request.body)
        debtor_username = data.get('debtor')
        amount = data.get('amount')

        # Get the debtor user object
        debtor = User.objects.get(username=debtor_username)

        # Create a new transaction to cancel the debt
        Transaction.objects.create(
            creditor=debtor,  # The debtor becomes the creditor
            debtor=request.user,  # The current user becomes the debtor
            amount=amount,
            description="Debt cancellation"
        )

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_http_methods(["GET"])
@login_required
def get_payment_method(request, username):
    try:
        user = User.objects.get(username=username)
        payment_method = user.profile.preferred_payment_method
        bank_account = user.profile.bank_account if payment_method == 'bank_transfer' else None
        return JsonResponse({
            'status': 'success',
            'payment_method': payment_method if payment_method else 'Not specified',
            'bank_account': bank_account
        })
    except User.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'User not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_http_methods(["POST"])
@csrf_protect
@login_required
def repay_debt(request):
    try:
        data = json.loads(request.body)
        creditor_username = data.get('creditor')
        amount = data.get('amount')
        payment_method = data.get('payment_method')

        # Get the creditor user object
        creditor = User.objects.get(username=creditor_username)

        # Create a payment verification record without creating a transaction yet
        verification = PaymentVerification.objects.create(
            transaction=None,  # No transaction yet
            payer=request.user,
            receiver=creditor,
            amount=amount,
            payment_method=payment_method
        )

        # Create notification for the creditor to verify the payment
        create_notification(
            user=creditor,
            notification_type='payment',
            title=f'Payment Verification Required ({payment_method})',
            message=f'{request.user.username} claims to have paid you ${amount} via {payment_method}. Please verify this payment.',
            send_email=True,
            verification_id=verification.id  # Include the verification ID
        )

        return JsonResponse({
            'status': 'pending',
            'message': 'Payment verification request sent to the creditor.'
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_http_methods(["POST"])
@csrf_protect
@login_required
def verify_payment(request):
    try:
        data = json.loads(request.body)
        print("Received data:", data)  # Debug log
        notification_id = data.get('notification_id')
        action = data.get('action')  # 'verify' or 'reject'
        print(f"Notification ID: {notification_id}, Action: {action}")  # Debug log

        # Get the notification
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
        print("Found notification:", notification)  # Debug log

        # Extract verification ID from the notification message
        verification_id = notification.verification_id
        print("Verification ID:", verification_id)  # Debug log

        # Get the verification record
        verification = get_object_or_404(PaymentVerification, 
            id=verification_id,
            receiver=request.user,
            status='pending'
        )
        print("Found verification:", verification)  # Debug log
        
        if action == 'verify':
            # Create the actual transaction only upon verification
            transaction = Transaction.objects.create(
                creditor=verification.payer,  # The payer becomes the creditor
                debtor=verification.receiver,  # The receiver becomes the debtor
                amount=verification.amount,
                description=f"Debt repayment via {verification.payment_method} (verified)"
            )

            # Update verification record
            verification.transaction = transaction
            verification.status = 'verified'
            verification.verified_at = timezone.now()
            verification.save()

            create_notification(
                user=verification.payer,
                notification_type='payment',
                title='Payment Verified',
                message=f'{request.user.username} has verified your payment of ${verification.amount}.',
                send_email=True
            )

            return JsonResponse({'status': 'success', 'message': 'Payment verified successfully'})
        elif action == 'reject':
            verification.status = 'rejected'
            verification.save()

            create_notification(
                user=verification.payer,
                notification_type='payment',
                title='Payment Rejected',
                message=f'{request.user.username} has rejected your payment of ${verification.amount}. Please contact them for clarification.',
                send_email=True
            )

            return JsonResponse({'status': 'success', 'message': 'Payment rejected'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)
    except Notification.DoesNotExist:
        print("Notification not found for ID:", notification_id)  # Debug log
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)
    except PaymentVerification.DoesNotExist:
        print("Verification not found for ID:", verification_id)  # Debug log
        return JsonResponse({'status': 'error', 'message': 'Verification not found'}, status=404)
    except Exception as e:
        print("Error in verify_payment:", str(e))  # Debug log
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)