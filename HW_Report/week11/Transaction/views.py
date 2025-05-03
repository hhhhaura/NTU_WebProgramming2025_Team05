from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Transaction
from decimal import Decimal

# Create your views here.
@login_required(login_url="/user/login/")
def history(request):

    '''
    # Fetch all transactions and users
    transactions = Transaction.objects.all()
    users = User.objects.all()
    # Calculate total debt in both directions
    debt_map = {}
    for trans in transactions:
        creditor = trans.creditor.username
        debtor = trans.debtor.username
        amount = Decimal(str(trans.amount))  # Convert to Decimal for precision

        if creditor == debtor:
            continue  # Skip self-payments

        # Create a consistent key where the smaller name alphabetically comes first
        key = '->'.join(sorted([creditor, debtor]))

        if key not in debt_map:
            debt_map[key] = {
                creditor: Decimal('0'),
                debtor: Decimal('0')
            }

        # Add to creditor's balance (positive means they are owed money)
        debt_map[key][creditor] += amount
        # Add to debtor's balance (negative means they owe money)
        debt_map[key][debtor] -= amount

    # Prepare debt data for the template
    debts = []
    for key, balances in debt_map.items():
        person1, person2 = key.split('->')
        net_amount = balances[person1]

        # Only include non-zero balances
        if abs(net_amount) > Decimal('0.01'):
            if net_amount > 0:
                debtor, creditor, amount = person2, person1, net_amount
            else:
                debtor, creditor, amount = person1, person2, abs(net_amount)
            debts.append({
                'debtor': debtor,
                'creditor': creditor,
                'amount': f"{amount:.2f}"  # Format to 2 decimal places
            })
    '''
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
            messages.success(request, 'Transaction added successfully!')
            return redirect('/transaction/history')  # Assuming you want to go back to history
        except User.DoesNotExist:
            messages.error(request, 'Selected creditor does not exist.')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'add_transaction.html', {'users': users})