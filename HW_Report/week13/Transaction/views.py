from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Transaction
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

# Create your views here.
@login_required(login_url="/user/login/")
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

@login_required(login_url="/user/login/")
def single_transaction(request, slug):
    trans = Transaction.objects.get(slug=slug)
    return render(request,'single_history.html', {'trans': trans})

@login_required(login_url="/user/login/")
def add_transaction(request):
    if request.method == 'POST':
        # Verify reCAPTCHA
        recaptcha_response = request.POST.get('g-recaptcha-response')
        if not recaptcha_response:
            messages.error(request, 'Please complete the reCAPTCHA.')
            users = User.objects.exclude(id=request.user.id)
            return render(request, 'add_transaction.html', {'users': users})

        # Verify the reCAPTCHA response with Google
        verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        data = {
            'secret': '6LcRqTcrAAAAAOum1axN3iqetO0ymUv9Dbvp6OP1',  # Replace with your secret key
            'response': recaptcha_response
        }
        response = requests.post(verify_url, data=data)
        result = response.json()

        if not result.get('success', False):
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            users = User.objects.exclude(id=request.user.id)
            return render(request, 'add_transaction.html', {'users': users})

        creditor_id = request.POST.get('creditor')
        amount = request.POST.get('amount')
        description = request.POST.get('description', '')

        try:
            creditor = User.objects.get(id=creditor_id)

            if creditor == request.user:
                messages.error(request, "You can't owe yourself money.")
                return redirect('add_transaction')

            transaction = Transaction.objects.create(
                creditor=creditor,
                debtor=request.user,
                amount=amount,
                description=description
            )

            # Create notification for the creditor
            create_notification(
                user=creditor,
                notification_type='debt',
                title='New Debt Added',
                message=f'{request.user.username} has added a debt of ${amount} to you for: {description}',
                send_email=True
            )

            messages.success(request, 'Transaction added successfully!')
            return redirect('/transaction/add_transaction/')
        except User.DoesNotExist:
            messages.error(request, 'Selected creditor does not exist.')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'add_transaction.html', {'users': users})

@login_required(login_url="/user/login/")
def my_debt(request):
    print("[DEBUG] Entering my_debt view")
    print(f"[DEBUG] User: {request.user}")
    
    # Create a factory for requests
    factory = APIRequestFactory()
    
    # Get debt relationships directly from the API view
    debt_view = DebtRelationshipAPIView.as_view()
    api_request = factory.get('/api/debts/')
    api_request.user = request.user  # Pass the authenticated user
    debt_response = debt_view(api_request)
    print(f"[DEBUG] Debt response: {debt_response.data}")
    debts = debt_response.data if debt_response.status_code == 200 else []

    # Get total balance directly from the API view
    total_view = TotalDebtAPIView.as_view()
    api_request = factory.get('/api/debts/total/')
    api_request.user = request.user  # Pass the authenticated user
    total_response = total_view(api_request)
    total_balance = total_response.data if total_response.status_code == 200 else []

    return render(request, 'my_debt.html', {
        'debts': debts,
        'total_balance': total_balance
    })

@login_required(login_url="/user/login/")
@csrf_protect
@require_http_methods(["POST"])
def cancel_debt(request):
    try:
        data = json.loads(request.body)
        debtor = data.get('debtor')
        amount = data.get('amount')

        if not debtor or not amount:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Get the debtor user object
        try:
            debtor_user = User.objects.get(username=debtor)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Debtor not found'}, status=404)

        # Create a new transaction that cancels out the debt
        Transaction.objects.create(
            creditor=debtor_user,  # The debtor becomes the creditor
            debtor=request.user,   # The current user becomes the debtor
            amount=amount,         # Same amount to cancel it out
            description="Debt cancellation"
        )

        return JsonResponse({'message': 'Debt cancelled successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)