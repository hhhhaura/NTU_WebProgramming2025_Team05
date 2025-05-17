from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
import uuid

def generate_random_slug():
    return get_random_string(length=10)

class SharedExpense(models.Model):
    paid_by = models.ForeignKey(
        User,
        related_name='expenses_paid',
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    shared_with = models.ManyToManyField(
        User,
        related_name='shared_expenses',
        through='ExpenseShare'
    )
    slug = models.CharField(
        max_length=10,
        unique=True,
        default=generate_random_slug,
        editable=False
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Expense of ${self.amount} paid by {self.paid_by.username}'

    def save(self, *args, **kwargs):
        if not self.slug:
            while True:
                slug = generate_random_slug()
                if not SharedExpense.objects.filter(slug=slug).exists():
                    self.slug = slug
                    break
        super().save(*args, **kwargs)
        
        # Broadcast to WebSocket group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "transactions",
            {
                "type": "transaction_update",
            }
        )

class ExpenseShare(models.Model):
    expense = models.ForeignKey(SharedExpense, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s share of ${self.share_amount} for {self.expense}"

class Transaction(models.Model):
    creditor = models.ForeignKey(
        User,
        related_name='transactions_given',
        on_delete=models.CASCADE)

    debtor = models.ForeignKey(
        User,
        related_name='transactions_received',
        on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(
        max_length=10,
        unique=True,
        default=generate_random_slug,
        editable=False
    )
    shared_expense = models.ForeignKey(
        SharedExpense,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resulting_transactions'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.debtor.username} owes {self.creditor.username} ${self.amount}'

    def save(self, *args, **kwargs):
        if not self.slug:
            while True:
                slug = generate_random_slug()
                if not Transaction.objects.filter(slug=slug).exists():
                    self.slug = slug
                    break
        super().save(*args, **kwargs)

        # Broadcast to WebSocket group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "transactions",
            {
                "type": "transaction_update",
            }
        )

class PaymentVerification(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected')
    )

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='verifications', null=True, blank=True)
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_made')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('line_pay', 'Line Pay'), 
        ('bank_transfer', 'Bank Transfer')
    )
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment verification for ${self.amount} from {self.payer.username} to {self.receiver.username}"